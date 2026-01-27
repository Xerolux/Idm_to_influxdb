<template>
    <div class="space-y-3 overflow-y-auto">
        <div v-if="loading" class="text-center py-8 text-gray-500">
            <i class="pi pi-spin pi-spinner text-2xl"></i>
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm">
            {{ error }}
        </div>

        <div v-for="(categoryMetrics, category) in filteredMetrics" :key="category" class="bg-white rounded-lg p-3 shadow-sm border border-gray-200">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2 flex items-center gap-2">
                <i :class="getCategoryIcon(category)"></i>
                {{ getCategoryLabel(category) }}
            </h3>
            <div class="space-y-1">
                <MetricRow
                    v-for="metric in categoryMetrics"
                    :key="metric.name"
                    :metric="metric"
                    :value="currentValues[metric.name]?.value"
                    @dragstart="onMetricDragStart"
                />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import axios from 'axios';
import { useWebSocket } from '../utils/websocket.js';
import { useHeatpumpsStore } from '@/stores/heatpumps';
import MetricRow from './MetricRow.vue';

const emit = defineEmits(['sensor-drag-start']);
const hpStore = useHeatpumpsStore();

const metrics = ref({
    temperature: [],
    power: [],
    pressure: [],
    energy: [],
    flow: [],
    status: [],
    mode: [],
    control: [],
    state: [],
    ai: [],
    other: []
});

const currentValues = ref({});
const loading = ref(true);
const error = ref(null);
let refreshTimer = null;

const handleMetricUpdate = (data) => {
    const activePrefix = hpStore.activeHeatpumpId ? `${hpStore.activeHeatpumpId}.` : '';

    const updatePoint = (point) => {
        if (!point || !point.metric) return;

        let metricName = point.metric;

        // Strip prefix if present
        if (activePrefix && metricName.startsWith(activePrefix)) {
            metricName = metricName.substring(activePrefix.length);
        } else if (hpStore.activeHeatpumpId && !activePrefix) {
             // If we have an active HP but no prefix logic (should not happen if logic correct), ignore?
             // Or if message has no prefix?
        }

        if (!currentValues.value[metricName]) {
            currentValues.value[metricName] = {
                value: point.value,
                timestamp: point.timestamp
            };
        } else {
            currentValues.value[metricName].value = point.value;
            currentValues.value[metricName].timestamp = point.timestamp;
        }
    };

    if (data.metric) {
        updatePoint(data);
    } else {
        Object.values(data).forEach(updatePoint);
    }
};

const { subscribe, unsubscribe } = useWebSocket(handleMetricUpdate);

const filteredMetrics = computed(() => {
    const filtered = {};
    for (const [key, val] of Object.entries(metrics.value)) {
        if (val && val.length > 0) {
            filtered[key] = val;
        }
    }
    return filtered;
});

const loadMetrics = async () => {
    try {
        const res = await axios.get('/api/metrics/available');
        metrics.value = res.data;
    } catch (e) {
        error.value = 'Fehler beim Laden der Metriken';
        console.error(e);
    }
};

const loadCurrentValues = async () => {
    try {
        let url = '/api/data'; // Default (legacy or default HP)
        if (hpStore.activeHeatpumpId) {
            url = `/api/data/${hpStore.activeHeatpumpId}`;
        }

        const res = await axios.get(url);

        // Convert flat values to object with timestamp
        const data = {};
        const now = Date.now() / 1000;

        for (const [key, value] of Object.entries(res.data)) {
            data[key] = { value, timestamp: now };
        }

        currentValues.value = data;
        loading.value = false;
        error.value = null;
    } catch (e) {
        error.value = 'Fehler beim Laden der Werte';
        console.error(e);
    }
};

const getCategoryLabel = (category) => {
    const labels = {
        temperature: 'Temperaturen',
        power: 'Leistung',
        pressure: 'Druck',
        energy: 'Energie',
        flow: 'Durchfluss',
        status: 'Status',
        mode: 'Modi',
        control: 'Steuerung',
        state: 'Zustand',
        ai: 'KI-Analyse',
        other: 'Sonstige'
    };
    return labels[category] || category;
};

const getCategoryIcon = (category) => {
    const icons = {
        temperature: 'pi pi-sun text-orange-500',
        power: 'pi pi-bolt text-yellow-500',
        pressure: 'pi pi-bars text-teal-500',
        energy: 'pi pi-chart-line text-green-500',
        flow: 'pi pi-arrow-right text-cyan-500',
        status: 'pi pi-info-circle text-blue-500',
        mode: 'pi pi-cog text-gray-500',
        control: 'pi pi-sliders-h text-purple-500',
        state: 'pi pi-check-circle text-emerald-500',
        ai: 'pi pi-sparkles text-purple-500',
        other: 'pi pi-box text-gray-400'
    };
    return icons[category] || 'pi pi-circle';
};

const onMetricDragStart = (metric) => {
    emit('sensor-drag-start', metric);
};

const getSubscribedMetrics = () => {
    const allMetrics = [];
    if (metrics.value) {
        Object.values(metrics.value).forEach(list => {
            if (Array.isArray(list)) {
                list.forEach(m => allMetrics.push(m.name));
            }
        });
    }

    if (hpStore.activeHeatpumpId) {
        return allMetrics.map(m => `${hpStore.activeHeatpumpId}.${m}`);
    }
    return allMetrics;
};

const updateSubscriptions = () => {
    const allMetrics = getSubscribedMetrics();
    if (allMetrics.length > 0) {
        subscribe(allMetrics);
    }
}

onMounted(() => {
    loadMetrics().then(() => {
        updateSubscriptions();
    });
    loadCurrentValues();
    refreshTimer = setInterval(loadCurrentValues, 60000);
});

watch(() => hpStore.activeHeatpumpId, () => {
    loadCurrentValues();
    updateSubscriptions();
});

onUnmounted(() => {
    if (refreshTimer) clearInterval(refreshTimer);
    const allMetrics = getSubscribedMetrics();
    if (allMetrics.length > 0) {
        unsubscribe(allMetrics);
    }
});
</script>

<style scoped>
/* Scrollbar styling */
::-webkit-scrollbar {
    width: 4px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
</style>
