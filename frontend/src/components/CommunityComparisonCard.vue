<template>
    <div class="bg-white rounded-lg p-4 h-full flex flex-col shadow-sm border border-gray-200 relative">
        <div class="flex justify-between items-start mb-3">
            <div>
                <h3 class="text-gray-900 font-bold text-sm flex items-center gap-2">
                    <i class="pi pi-users text-blue-500"></i>
                    {{ t('telemetry.comparison') }}
                </h3>
                <span class="text-xs text-gray-500">{{ metricLabel }}</span>
            </div>

            <div class="flex gap-1">
                 <button
                    @click="refreshData"
                    class="text-gray-400 hover:text-gray-600 p-1"
                    :class="{ 'animate-spin': loading }"
                    :title="t('status')"
                >
                    <i class="pi pi-refresh text-xs"></i>
                </button>
            </div>
        </div>

        <div v-if="loading && !chartData.labels.length" class="flex-grow flex items-center justify-center">
            <i class="pi pi-spin pi-spinner text-2xl text-gray-400"></i>
        </div>

        <div v-else-if="error" class="flex-grow flex items-center justify-center text-red-500 text-xs p-2 text-center">
            {{ error }}
        </div>

        <div v-else class="flex-grow relative min-h-[150px]">
            <Bar :data="chartData" :options="chartOptions" />
        </div>

        <div v-if="stats && !loading" class="mt-2 text-xs text-gray-500 flex justify-between px-2">
             <span>{{ t('telemetry.range') }}: {{ stats.min }} - {{ stats.max }}</span>
             <span>n={{ stats.n }}</span>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'vue-chartjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const { t } = useI18n();

const props = defineProps({
    metric: { type: String, default: 'cop_current' },
    title: { type: String, default: '' },
    chartId: { type: String, default: 'comparison-chart' }
});

const loading = ref(false);
const error = ref(null);
const localValue = ref(0);
const communityStats = ref({ avg: 0, min: 0, max: 0 });
const sampleSize = ref(0);
const modelName = ref('');

const metricLabel = computed(() => {
    if (props.title) return props.title;
    // Simple formatting if no title provided
    return props.metric.replace(/_/g, ' ').toUpperCase();
});

const chartData = computed(() => {
    return {
        labels: [t('telemetry.yourValue'), t('telemetry.communityAvg')],
        datasets: [
            {
                label: metricLabel.value,
                data: [localValue.value, communityStats.value.avg],
                backgroundColor: ['#3b82f6', '#8b5cf6'],
                borderRadius: 4,
                barPercentage: 0.6
            }
        ]
    };
});

const chartOptions = computed(() => {
    const isDark = document.documentElement.classList.contains('my-app-dark');
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: (context) => {
                         let label = context.dataset.label || '';
                         if (label) {
                             label += ': ';
                         }
                         if (context.parsed.y !== null) {
                             label += context.parsed.y.toFixed(2);
                         }
                         return label;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: isDark ? '#374151' : '#f0f0f0'
                },
                ticks: {
                     color: isDark ? '#9ca3af' : '#666',
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                     color: isDark ? '#9ca3af' : '#666',
                }
            }
        }
    };
});

const stats = computed(() => ({
    min: communityStats.value.min?.toFixed(2) || '-',
    max: communityStats.value.max?.toFixed(2) || '-',
    n: sampleSize.value
}));

const fetchData = async () => {
    loading.value = true;
    error.value = null;

    try {
        // 1. Get Config for Model (if not loaded)
        if (!modelName.value) {
            const configRes = await axios.get('/api/config');
            modelName.value = configRes.data.heatpump_model;

            if (!modelName.value) {
                error.value = "Model not configured";
                loading.value = false;
                return;
            }
        }

        // 2. Get Community Data
        const communityRes = await axios.get('/api/telemetry/community/averages', {
            params: {
                model: modelName.value,
                metrics: props.metric
            }
        });

        if (communityRes.data.metrics && communityRes.data.metrics[props.metric]) {
            const mData = communityRes.data.metrics[props.metric];
            communityStats.value = {
                avg: parseFloat(mData.avg || 0),
                min: parseFloat(mData.min || 0),
                max: parseFloat(mData.max || 0)
            };
            sampleSize.value = communityRes.data.sample_size || 0;
        }

        // 3. Get Local Data
        const localRes = await axios.get('/api/metrics/current');
        if (localRes.data[props.metric]) {
            localValue.value = parseFloat(localRes.data[props.metric].value || 0);
        }

    } catch (err) {
        console.error("Comparison data fetch failed:", err);
        // Handle 401/403 specifically if needed
        if (err.response && err.response.status === 401) {
             error.value = t('telemetry.enableSharing');
        } else {
             error.value = t('error');
        }
    } finally {
        loading.value = false;
    }
};

const refreshData = () => {
    fetchData();
};

onMounted(() => {
    fetchData();
});

watch(() => props.metric, () => {
    fetchData();
});

</script>
