<template>
    <Dialog
        v-model:visible="visible"
        modal
        header="Dashboard exportieren"
        :style="{ width: '90vw', maxWidth: '500px' }"
    >
        <div class="space-y-4">
            <!-- Format Selection -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Format</label>
                <div class="grid grid-cols-2 gap-3">
                    <button
                        @click="selectedFormat = 'png'"
                        :class="[
                            'p-4 rounded-lg border-2 text-center transition-all',
                            selectedFormat === 'png'
                                ? 'border-blue-500 bg-blue-50 text-blue-700'
                                : 'border-gray-200 hover:border-gray-300'
                        ]"
                    >
                        <i class="pi pi-image text-2xl mb-2"></i>
                        <div class="font-medium">PNG</div>
                        <div class="text-xs text-gray-500 mt-1">Bild-Datei</div>
                    </button>
                    <button
                        @click="selectedFormat = 'pdf'"
                        :class="[
                            'p-4 rounded-lg border-2 text-center transition-all',
                            selectedFormat === 'pdf'
                                ? 'border-blue-500 bg-blue-50 text-blue-700'
                                : 'border-gray-200 hover:border-gray-300'
                        ]"
                    >
                        <i class="pi pi-file-pdf text-2xl mb-2"></i>
                        <div class="font-medium">PDF</div>
                        <div class="text-xs text-gray-500 mt-1">Dokument</div>
                    </button>
                </div>
            </div>

            <!-- Quality Options (PNG only) -->
            <div v-if="selectedFormat === 'png'">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Qualität: {{ scale }}x
                </label>
                <input
                    v-model.number="scale"
                    type="range"
                    min="1"
                    max="4"
                    step="0.5"
                    class="w-full"
                />
                <div class="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Klein</span>
                    <span>Standard</span>
                    <span>Hoch</span>
                </div>
            </div>

            <!-- Info -->
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <div class="flex items-start gap-2">
                    <i class="pi pi-info-circle text-blue-600 mt-0.5"></i>
                    <div class="text-sm text-blue-800">
                        <p v-if="selectedFormat === 'png'">
                            PNG eignet sich für Präsentationen und Web.
                            {{ scale === 2 ? 'Standardqualität (2x).' : scale > 2 ? 'Hohe Qualität (' + scale + 'x) - größere Datei.' : 'Niedrige Qualität - kleine Datei.' }}
                        </p>
                        <p v-else>
                            PDF eignet sich für Dokumentation und Druck.
                            Automatisch an A4 (Querformat) angepasst.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <template #footer>
            <Button
                @click="visible = false"
                label="Abbrechen"
                severity="secondary"
                text
            />
            <Button
                @click="handleExport"
                :label="exporting ? 'Exportiere...' : 'Exportieren'"
                :icon="exporting ? 'pi pi-spinner pi-spin' : 'pi pi-download'"
                severity="primary"
                :disabled="exporting"
            />
        </template>
    </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import { exportDashboard } from '../utils/dashboardExport';

const props = defineProps({
    modelValue: { type: Boolean, default: false },
    dashboardName: { type: String, default: 'Dashboard' },
    dashboardElement: { type: Object, default: null }
});

const emit = defineEmits(['update:modelValue']);

const visible = ref(props.modelValue);
const selectedFormat = ref('png');
const scale = ref(2);
const exporting = ref(false);

const handleExport = async () => {
    if (!props.dashboardElement) {
        console.error('No dashboard element provided');
        return;
    }

    exporting.value = true;

    try {
        await new Promise(resolve => setTimeout(resolve, 100)); // Small delay to show spinner

        await exportDashboard(
            props.dashboardElement,
            selectedFormat.value,
            props.dashboardName,
            {
                scale: scale.value
            }
        );

        visible.value = false;
    } catch (error) {
        console.error('Export failed:', error);
        // Could show error toast here
    } finally {
        exporting.value = false;
    }
};

watch(() => props.modelValue, (val) => {
    visible.value = val;
});

watch(visible, (val) => {
    emit('update:modelValue', val);
});
</script>

<style scoped>
/* Add any specific styles if needed */
</style>
