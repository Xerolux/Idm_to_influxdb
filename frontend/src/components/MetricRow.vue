<template>
    <div
        class="flex justify-between items-center text-sm p-1.5 rounded hover:bg-gray-50 cursor-grab active:cursor-grabbing group transition-colors"
        draggable="true"
        @dragstart="onDragStart"
    >
        <div class="flex flex-col min-w-0">
            <span class="text-gray-700 font-medium truncate" :title="metric.display">{{ metric.display }}</span>
            <span class="text-[10px] text-gray-400 font-mono truncate">{{ metric.name }}</span>
        </div>
        <span class="font-mono font-bold whitespace-nowrap ml-2" :class="valueClass">
             {{ formattedValue }}
             <span class="text-[10px] text-gray-400 font-normal">{{ unit }}</span>
        </span>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    metric: {
        type: Object,
        required: true
    },
    value: {
        type: [Number, String, Boolean],
        default: null
    }
});

const emit = defineEmits(['dragstart']);

const onDragStart = (event) => {
    event.dataTransfer.setData('application/json', JSON.stringify(props.metric));
    event.dataTransfer.effectAllowed = 'copy';
    emit('dragstart', props.metric);
};

const unit = computed(() => {
    const name = props.metric.name;
    if (name.includes('temp')) return '°C';
    if (name.includes('power')) return 'W';
    if (name.includes('pressure')) return 'bar';
    if (name.includes('energy')) return 'kWh';
    if (name.includes('flow')) return 'l/min';
    if (name.includes('score')) return '%';
    return '';
});

const formattedValue = computed(() => {
    const v = props.value;
    const name = props.metric.name;
    if (v === undefined || v === null) return '-';

    // AI Scores
    if (name.includes('score')) {
        return Number(v).toFixed(4);
    }

    // Status/Mode mapping
    if (name.includes('status') || name.includes('mode') || name.includes('flag')) {
         const num = Number(v);
         // Simple mapping for common states
         if (name.includes('status_heat_pump')) {
             if (num === 0) return 'Aus';
             if (num === 1) return 'Heizen';
             if (num === 2) return 'Kühlen';
             if (num === 4) return 'WW';
             if (num === 8) return 'Abtauen';
         }

         // Generic boolean/flag mapping
         if (num === 0) return name.includes('flag') ? 'NEIN' : 'Aus';
         if (num === 1) return name.includes('flag') ? 'JA' : 'Ein';

         return num;
    }

    return Number(v).toFixed(1);
});

const valueClass = computed(() => {
    const v = props.value;
    const name = props.metric.name;

    if (v === undefined || v === null) return 'text-gray-400';

    if (name.includes('temp')) {
        const num = Number(v);
        if (num < 0) return 'text-blue-600';
        if (num > 50) return 'text-red-600';
        if (num > 25) return 'text-orange-500';
        return 'text-green-600';
    }

    if (name.includes('status') || name.includes('flag')) {
        return Number(v) > 0 ? 'text-blue-600' : 'text-gray-500';
    }

    return 'text-gray-800';
});
</script>
