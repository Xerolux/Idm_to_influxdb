<template>
    <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-2">
            <label class="font-bold">Select Date</label>
            <input
                type="date"
                v-model="selectedDate"
                class="p-inputtext p-component w-full md:w-auto"
            />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="p-4 bg-gray-900/50 rounded border border-gray-700 flex flex-col gap-2">
                <div class="text-sm text-gray-400">Level 1 (User)</div>
                <div class="flex items-center justify-between">
                    <div class="text-3xl font-mono font-bold text-green-400 tracking-wider">{{ codeLevel1 }}</div>
                    <i class="pi pi-user text-green-400/50 text-2xl"></i>
                </div>
                <div class="text-xs text-gray-500">Format: DDMM</div>
            </div>

            <div class="p-4 bg-gray-900/50 rounded border border-gray-700 flex flex-col gap-2">
                <div class="text-sm text-gray-400">Level 2 (Technician)</div>
                <div class="flex items-center justify-between">
                    <div class="text-3xl font-mono font-bold text-yellow-400 tracking-wider">{{ codeLevel2 }}</div>
                    <i class="pi pi-cog text-yellow-400/50 text-2xl"></i>
                </div>
                <div class="text-xs text-gray-500">Daily changing code</div>
            </div>
        </div>

        <div class="p-3 bg-blue-900/20 border border-blue-800 rounded text-sm text-blue-200">
            <div class="flex gap-2">
                <i class="pi pi-info-circle mt-0.5"></i>
                <div>
                    These codes are calculated based on the selected date.
                    <br>
                    <span class="opacity-70 text-xs">Algorithm derived from public information (IDM heat pump community). Use at your own risk.</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Default to today
const selectedDate = ref(new Date().toISOString().split('T')[0]);

const codeLevel1 = computed(() => {
    if (!selectedDate.value) return '----';
    // Parse manually to avoid timezone issues
    const parts = selectedDate.value.split('-');
    const day = parts[2];
    const month = parts[1];
    return `${day}${month}`;
});

const codeLevel2 = computed(() => {
    if (!selectedDate.value) return '-----';
    const parts = selectedDate.value.split('-');
    const year = parseInt(parts[0]);
    const month = parseInt(parts[1]);
    const day = parseInt(parts[2]);

    // Algorithm:
    // Base 62391 + 4 * (Day + 31 * Month + 372 * (Year - 2000))
    // Note: 372 = 12 * 31

    const year2digit = year % 100;

    const val = day + (31 * month) + (372 * year2digit);
    const code = 62391 + (4 * val);

    return code;
});
</script>
