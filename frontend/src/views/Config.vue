<template>
    <div class="p-4 flex flex-col gap-4">
        <h1 class="text-2xl font-bold mb-4">Configuration</h1>

        <div v-if="loading" class="flex justify-center">
            <i class="pi pi-spin pi-spinner text-4xl"></i>
        </div>

        <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card class="bg-gray-800 text-white">
                <template #title>IDM Heat Pump</template>
                <template #content>
                    <div class="flex flex-col gap-4">
                        <div class="flex flex-col gap-2">
                            <label>Host / IP</label>
                            <InputText v-model="config.idm.host" />
                        </div>
                        <div class="flex flex-col gap-2">
                            <label>Port</label>
                            <InputNumber v-model="config.idm.port" :useGrouping="false" />
                        </div>

                        <div class="flex flex-col gap-2">
                            <label class="font-bold">Enabled Features</label>
                            <div class="flex flex-col gap-2 p-2 border border-gray-700 rounded bg-gray-900/50">
                                <div class="flex items-center gap-2">
                                    <Checkbox v-model="config.idm.circuits" inputId="circuitA" value="A" disabled />
                                    <label for="circuitA" class="opacity-50">Circuit A (Always On)</label>
                                </div>
                                <div class="flex flex-wrap gap-4">
                                    <div v-for="c in ['B', 'C', 'D', 'E', 'F', 'G']" :key="c" class="flex items-center gap-2">
                                        <Checkbox v-model="config.idm.circuits" :inputId="'circuit'+c" :value="c" />
                                        <label :for="'circuit'+c">Circuit {{ c }}</label>
                                    </div>
                                </div>
                            </div>
                            <div class="flex flex-col gap-2 p-2 border border-gray-700 rounded bg-gray-900/50">
                                <label class="text-sm text-gray-400">Zone Modules</label>
                                <div class="flex flex-wrap gap-4">
                                    <div v-for="z in 10" :key="z" class="flex items-center gap-2">
                                        <Checkbox v-model="config.idm.zones" :inputId="'zone'+(z-1)" :value="(z-1)" />
                                        <label :for="'zone'+(z-1)">Zone {{ z }}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </Card>

            <Card class="bg-gray-800 text-white">
                <template #title>InfluxDB</template>
                <template #content>
                    <div class="flex flex-col gap-4">
                         <div class="flex flex-col gap-2">
                            <label>URL</label>
                            <InputText v-model="config.influx.url" />
                        </div>
                        <div class="flex flex-col gap-2">
                            <label>Organization</label>
                            <InputText v-model="config.influx.org" />
                        </div>
                         <div class="flex flex-col gap-2">
                            <label>Bucket</label>
                            <InputText v-model="config.influx.bucket" />
                        </div>
                    </div>
                </template>
            </Card>

            <Card class="bg-gray-800 text-white">
                <template #title>Data Collection</template>
                <template #content>
                     <div class="flex flex-col gap-4">
                         <div class="flex items-center gap-2">
                             <Checkbox v-model="config.logging.realtime_mode" binary inputId="realtime_mode" />
                             <label for="realtime_mode">Realtime Mode (1 second interval)</label>
                         </div>
                         <div class="flex flex-col gap-2" v-if="!config.logging.realtime_mode">
                             <label>Polling Interval (seconds)</label>
                             <InputNumber v-model="config.logging.interval" :min="1" :max="3600" :useGrouping="false" />
                             <small class="text-gray-400">How often to read data from heat pump (1-3600 seconds)</small>
                         </div>
                     </div>
                </template>
            </Card>

            <Card class="bg-gray-800 text-white">
                <template #title>Web Interface</template>
                <template #content>
                     <div class="flex flex-col gap-4">
                         <div class="flex items-center gap-2">
                             <Checkbox v-model="config.web.write_enabled" binary inputId="write_enabled" />
                             <label for="write_enabled">Enable Write Access (Manual Control & Schedule)</label>
                         </div>
                     </div>
                </template>
            </Card>

            <Card class="bg-gray-800 text-white">
                <template #title>Admin Security</template>
                <template #content>
                    <div class="flex flex-col gap-4">
                        <div class="flex flex-col gap-2">
                             <label>New Password</label>
                             <InputText v-model="newPassword" type="password" />
                        </div>
                    </div>
                </template>
            </Card>

            <Card class="bg-gray-800 text-white">
                <template #title>
                    <div class="flex items-center gap-2">
                        <i class="pi pi-shield text-yellow-400"></i>
                        <span>Network Access Control</span>
                    </div>
                </template>
                <template #content>
                    <div class="flex flex-col gap-4">
                        <div class="flex items-center gap-2">
                            <Checkbox v-model="config.network_security.enabled" binary inputId="network_security_enabled" />
                            <label for="network_security_enabled" class="font-bold">Enable IP-based Access Control</label>
                        </div>

                        <div v-if="config.network_security.enabled" class="flex flex-col gap-4 p-3 border border-yellow-600 rounded bg-yellow-900/10">
                            <div class="flex items-start gap-2 text-yellow-400">
                                <i class="pi pi-exclamation-triangle mt-1"></i>
                                <small>Warning: Make sure your IP is whitelisted before enabling, or you will be locked out!</small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <label class="font-semibold">
                                    <i class="pi pi-check-circle text-green-400"></i> Whitelist (Allow these IPs)
                                </label>
                                <Textarea
                                    v-model="whitelistText"
                                    placeholder="192.168.1.0/24&#10;10.0.0.5&#10;172.16.0.0/16"
                                    rows="4"
                                    class="font-mono text-sm"
                                />
                                <small class="text-gray-400">
                                    One IP address or network (CIDR) per line. If whitelist is empty, all IPs are allowed (unless blacklisted).
                                    <br>Example: 192.168.1.0/24 allows 192.168.1.1 - 192.168.1.254
                                </small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <label class="font-semibold">
                                    <i class="pi pi-ban text-red-400"></i> Blacklist (Block these IPs)
                                </label>
                                <Textarea
                                    v-model="blacklistText"
                                    placeholder="203.0.113.0/24&#10;198.51.100.5"
                                    rows="4"
                                    class="font-mono text-sm"
                                />
                                <small class="text-gray-400">
                                    One IP address or network (CIDR) per line. Blacklist is checked first (blocks before whitelist).
                                </small>
                            </div>

                            <div class="p-3 bg-blue-900/30 border border-blue-600 rounded">
                                <div class="flex items-start gap-2">
                                    <i class="pi pi-info-circle text-blue-400 mt-1"></i>
                                    <div class="text-sm text-blue-200">
                                        <strong>Your current IP:</strong> {{ currentClientIP || 'Loading...' }}
                                        <br><small class="text-blue-300">Make sure to add this to the whitelist!</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </Card>
        </div>

        <div class="flex gap-4 mt-4">
            <Button label="Save Configuration" icon="pi pi-save" @click="saveConfig" :loading="saving" />
            <Button label="Restart Service" icon="pi pi-refresh" severity="danger" @click="confirmRestart" />
        </div>

        <Toast />
        <ConfirmDialog />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Checkbox from 'primevue/checkbox';
import Button from 'primevue/button';
import Textarea from 'primevue/textarea';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { computed } from 'vue';

const config = ref({
    idm: { host: '', port: 502, circuits: ['A'], zones: [] },
    influx: { url: '', org: '', bucket: '' },
    web: { write_enabled: false },
    logging: { interval: 60, realtime_mode: false },
    network_security: { enabled: false, whitelist: [], blacklist: [] }
});
const newPassword = ref('');
const whitelistText = ref('');
const blacklistText = ref('');
const currentClientIP = ref('');
const loading = ref(true);
const saving = ref(false);
const toast = useToast();
const confirm = useConfirm();

onMounted(async () => {
    try {
        const res = await axios.get('/api/config');
        config.value = res.data;

        // Convert whitelist/blacklist arrays to text
        if (config.value.network_security) {
            whitelistText.value = (config.value.network_security.whitelist || []).join('\n');
            blacklistText.value = (config.value.network_security.blacklist || []).join('\n');
        }

        // Get current client IP
        try {
            const ipRes = await axios.get('/api/health');
            currentClientIP.value = ipRes.data.client_ip || 'Unknown';
        } catch (e) {
            console.error('Failed to get client IP', e);
        }
    } catch (e) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load config', life: 3000 });
    } finally {
        loading.value = false;
    }
});

const saveConfig = async () => {
    saving.value = true;
    try {
        const payload = {
            idm_host: config.value.idm.host,
            idm_port: config.value.idm.port,
            circuits: config.value.idm.circuits,
            zones: config.value.idm.zones,
            influx_url: config.value.influx.url,
            influx_org: config.value.influx.org,
            influx_bucket: config.value.influx.bucket,
            write_enabled: config.value.web.write_enabled,
            logging_interval: config.value.logging.interval,
            realtime_mode: config.value.logging.realtime_mode,
            network_security_enabled: config.value.network_security?.enabled || false,
            network_security_whitelist: whitelistText.value,
            network_security_blacklist: blacklistText.value,
            new_password: newPassword.value || undefined
        };
        const res = await axios.post('/api/config', payload);
        toast.add({ severity: 'success', summary: 'Success', detail: res.data.message || 'Settings saved successfully', life: 3000 });
        newPassword.value = '';
    } catch (e) {
        toast.add({ severity: 'error', summary: 'Error', detail: e.response?.data?.error || e.message, life: 5000 });
    } finally {
        saving.value = false;
    }
};

const confirmRestart = () => {
    confirm.require({
        message: 'Are you sure you want to restart the service?',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: async () => {
            try {
                const res = await axios.post('/api/restart');
                toast.add({ severity: 'info', summary: 'Restarting', detail: res.data.message, life: 3000 });
            } catch (e) {
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to restart', life: 3000 });
            }
        }
    });
};
</script>
