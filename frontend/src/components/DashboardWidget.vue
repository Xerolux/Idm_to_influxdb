<script setup>
import { computed, defineProps } from 'vue';

const props = defineProps({
    title: String,
    value: [String, Number],
    unit: String,
    trend: {
        type: String,
        default: 'neutral' // up, down, neutral
    },
    status: {
        type: String,
        default: 'normal' // normal, warning, error, success
    }
});

const statusColor = computed(() => {
    switch (props.status) {
        case 'success': return 'text-success-400';
        case 'warning': return 'text-warning-400';
        case 'error': return 'text-error-400';
        default: return 'text-primary-400';
    }
});

const trendIcon = computed(() => {
    switch (props.trend) {
        case 'up': return 'pi pi-arrow-up';
        case 'down': return 'pi pi-arrow-down';
        default: return '';
    }
});

const trendColor = computed(() => {
    switch (props.trend) {
        case 'up': return 'text-success-400';
        case 'down': return 'text-error-400';
        default: return '';
    }
});
</script>

<template>
    <div class="h-full flex flex-col justify-between group hover:bg-gray-700/30 transition-all duration-300 rounded-lg p-2 -m-2">
        <div class="flex justify-between items-start">
            <div class="text-gray-400 text-xs sm:text-sm font-medium uppercase tracking-wider">{{ title }}</div>
            <i v-if="trendIcon" :class="[trendIcon, trendColor, 'text-xs opacity-0 group-hover:opacity-100 transition-opacity']"></i>
        </div>
        <div class="flex items-end justify-between">
            <div :class="['text-2xl sm:text-3xl font-bold my-2 truncate', statusColor]" :title="value">
                {{ value }}
            </div>
            <div class="text-sm text-gray-500 ml-2 self-end">{{ unit }}</div>
        </div>
        <div class="h-1 bg-gray-700 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-primary-500 to-primary-400 rounded-full animate-pulse-subtle" style="width: 75%"></div>
        </div>
    </div>
</template>
