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
        <span class="font-mono font-bold whitespace-nowrap ml-2" :class="getValueClass(metric.name, value?.value)">
             {{ formatValue(metric.name, value?.value) }}
             <span class="text-[10px] text-gray-400 font-normal">{{ getUnit(metric.name) }}</span>
        </span>
    </div>
</template>

<script setup>
const props = defineProps({
    metric: {
        type: Object,
        required: true
    },
    value: {
        type: Object,
        default: null
    }
});

const emit = defineEmits(['dragstart']);

const onDragStart = (event) => {
    event.dataTransfer.setData('application/json', JSON.stringify(props.metric));
    event.dataTransfer.effectAllowed = 'copy';
    emit('dragstart', event, props.metric);
};

const formatValue = (name, value) => {
    if (value === undefined || value === null) return '-';

    // AI Scores
    if (name.includes('score')) {
        return Number(value).toFixed(4);
    }

    // Status/Mode mapping
    if (name.includes('status') || name.includes('mode') || name.includes('flag')) {
         const num = Number(value);
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

    return Number(value).toFixed(1);
};

const getUnit = (name) => {
    if (name.includes('temp')) return '°C';
    if (name.includes('power')) return 'W'; // or kW based on scaling
    if (name.includes('pressure')) return 'bar';
    if (name.includes('energy')) return 'kWh';
    if (name.includes('flow')) return 'l/min'; // Assuming
    if (name.includes('score')) return '%';
    return '';
};

const getValueClass = (name, value) => {
    if (value === undefined || value === null) return 'text-gray-400';

    if (name.includes('temp')) {
        const num = Number(value);
        if (num < 0) return 'text-blue-600';
        if (num > 50) return 'text-red-600';
        if (num > 25) return 'text-orange-500';
        return 'text-green-600';
    }

    if (name.includes('status') || name.includes('flag')) {
        return Number(value) > 0 ? 'text-blue-600' : 'text-gray-500';
    }

    return 'text-gray-800';
};
</script>
