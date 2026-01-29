// Xerolux 2026
/**
 * Chart Templates for IDM Metrics Collector
 *
 * Pre-configured chart templates for common use cases.
 */

export const chartTemplates = [
  {
    id: 'temperature-overview',
    name: 'Temperaturübersicht',
    description: 'Alle wichtigen Temperaturen auf einen Blick',
    icon: 'pi pi-thermometer',
    category: 'temperature',
    charts: [
      {
        title: 'Wärmepumpe Temperaturen',
        queries: [
          { label: 'Aussen', query: 'idm_heatpump_temp_outside', color: '#3b82f6' },
          { label: 'Vorlauf', query: 'idm_heatpump_temp_heat_pump_flow', color: '#ef4444' },
          { label: 'Rücklauf', query: 'idm_heatpump_temp_heat_pump_return', color: '#f59e0b' }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Warmwasser Temperaturen',
        queries: [
          { label: 'WW oben', query: 'idm_heatpump_temp_water_heater_top', color: '#ef4444' },
          { label: 'WW unten', query: 'idm_heatpump_temp_water_heater_bottom', color: '#f59e0b' },
          { label: 'Sollwert', query: 'idm_heatpump_temp_water_target', color: '#22c55e' }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Speicher & Quelltemperaturen',
        queries: [
          { label: 'Pufferspeicher', query: 'idm_heatpump_temp_heat_storage', color: '#a855f7' },
          { label: 'Kältespeicher', query: 'idm_heatpump_temp_cold_storage', color: '#3b82f6' },
          {
            label: 'Quelle Eingang',
            query: 'idm_heatpump_temp_heat_source_input',
            color: '#06b6d4'
          },
          {
            label: 'Quelle Ausgang',
            query: 'idm_heatpump_temp_heat_source_output',
            color: '#14b8a6'
          }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Heizkreis A - Temperaturen',
        queries: [
          {
            label: 'Vorlauf Ist',
            query: 'idm_heatpump_temp_flow_current_circuit_a',
            color: '#ef4444'
          },
          {
            label: 'Vorlauf Soll',
            query: 'idm_heatpump_temp_flow_target_circuit_a',
            color: '#22c55e'
          },
          { label: 'Raum', query: 'idm_heatpump_temp_room_circuit_a', color: '#f59e0b' }
        ],
        hours: 24,
        yAxisMode: 'single'
      }
    ]
  },
  {
    id: 'power-analysis',
    name: 'Leistungsanalyse',
    description: 'Stromverbrauch und Wärmeleistung',
    icon: 'pi pi-bolt',
    category: 'power',
    charts: [
      {
        title: 'Leistung',
        queries: [
          {
            label: 'Leistungsaufnahme',
            query: 'idm_heatpump_power_current_draw',
            color: '#ef4444'
          },
          { label: 'Wärmeleistung', query: 'idm_heatpump_power_current', color: '#3b82f6' }
        ],
        hours: 24,
        yAxisMode: 'dual'
      },
      {
        title: 'Energie (kumuliert)',
        queries: [
          { label: 'Gesamt', query: 'idm_heatpump_energy_heat_total', color: '#3b82f6' },
          { label: 'Heizung', query: 'idm_heatpump_energy_heat_heating', color: '#22c55e' },
          { label: 'Warmwasser', query: 'idm_heatpump_energy_heat_total_water', color: '#f59e0b' }
        ],
        hours: 168,
        yAxisMode: 'single'
      },
      {
        title: 'COP Verlauf',
        queries: [
          {
            label: 'COP',
            query: 'idm_heatpump_power_current / idm_heatpump_power_current_draw',
            color: '#22c55e'
          }
        ],
        hours: 24,
        yAxisMode: 'single'
      }
    ]
  },
  {
    id: 'efficiency-monitor',
    name: 'Effizienz-Monitor',
    description: 'COP und Leistungszahl überwachen',
    icon: 'pi pi-chart-line',
    category: 'efficiency',
    charts: [
      {
        title: 'COP Verlauf',
        queries: [
          {
            label: 'COP',
            query: 'idm_heatpump_power_current / idm_heatpump_power_current_draw',
            color: '#22c55e'
          }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Temperatur & Leistung',
        queries: [
          { label: 'Aussentemperatur', query: 'idm_heatpump_temp_outside', color: '#3b82f6' },
          { label: 'Leistungsaufnahme', query: 'idm_heatpump_power_current_draw', color: '#ef4444' }
        ],
        hours: 24,
        yAxisMode: 'dual'
      },
      {
        title: 'Vorlauf-Heizkurve',
        queries: [
          { label: 'Aussen', query: 'idm_heatpump_temp_outside', color: '#3b82f6' },
          {
            label: 'Vorlauf Ist',
            query: 'idm_heatpump_temp_flow_current_circuit_a',
            color: '#ef4444'
          },
          {
            label: 'Vorlauf Soll',
            query: 'idm_heatpump_temp_flow_target_circuit_a',
            color: '#22c55e'
          }
        ],
        hours: 168,
        yAxisMode: 'single'
      }
    ]
  },
  {
    id: 'heating-circuit-a',
    name: 'Heizkreis A Detail',
    description: 'Detaillierte Ansicht Heizkreis A',
    icon: 'pi pi-home',
    category: 'heating',
    charts: [
      {
        title: 'Heizkreis A - Temperaturen',
        queries: [
          {
            label: 'Vorlauf Ist',
            query: 'idm_heatpump_temp_flow_current_circuit_a',
            color: '#ef4444'
          },
          {
            label: 'Vorlauf Soll',
            query: 'idm_heatpump_temp_flow_target_circuit_a',
            color: '#22c55e'
          },
          { label: 'Raum', query: 'idm_heatpump_temp_room_circuit_a', color: '#f59e0b' }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Heizkurve',
        queries: [
          { label: 'Aussen', query: 'idm_heatpump_temp_outside', color: '#3b82f6' },
          {
            label: 'Vorlauf Soll',
            query: 'idm_heatpump_temp_flow_target_circuit_a',
            color: '#22c55e'
          }
        ],
        hours: 168,
        yAxisMode: 'single'
      },
      {
        title: 'Raumtemperatur Verlauf',
        queries: [{ label: 'Raum', query: 'idm_heatpump_temp_room_circuit_a', color: '#f59e0b' }],
        hours: 168,
        yAxisMode: 'single'
      }
    ]
  },
  {
    id: 'warmwater-monitor',
    name: 'Warmwasser-Monitor',
    description: 'Warmwasser-Temperaturen und -Verbrauch',
    icon: 'pi pi pi-volume-up',
    category: 'warmwater',
    charts: [
      {
        title: 'Warmwasser Temperaturen',
        queries: [
          { label: 'WW oben', query: 'idm_heatpump_temp_water_heater_top', color: '#ef4444' },
          { label: 'WW unten', query: 'idm_heatpump_temp_water_heater_bottom', color: '#f59e0b' },
          { label: 'Sollwert', query: 'idm_heatpump_temp_water_target', color: '#22c55e' }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Warmwasser Energie',
        queries: [
          { label: 'WW Energie', query: 'idm_heatpump_energy_heat_total_water', color: '#f59e0b' }
        ],
        hours: 168,
        yAxisMode: 'single'
      }
    ]
  },
  {
    id: 'solar-integration',
    name: 'Solar-Integration',
    description: 'Solaranlage und Speicher',
    icon: 'pi pi-sun',
    category: 'solar',
    charts: [
      {
        title: 'Solarkollektor Temperaturen',
        queries: [
          { label: 'Kollektor 1', query: 'idm_heatpump_temp_collector_1', color: '#f59e0b' },
          { label: 'Kollektor 2', query: 'idm_heatpump_temp_collector_2', color: '#ef4444' },
          { label: 'Speicher', query: 'idm_heatpump_temp_heat_storage', color: '#a855f7' }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Speicherladung',
        queries: [
          { label: 'Speicher', query: 'idm_heatpump_temp_heat_storage', color: '#a855f7' },
          { label: 'Vorlauf', query: 'idm_heatpump_temp_heat_pump_flow', color: '#ef4444' }
        ],
        hours: 24,
        yAxisMode: 'single'
      }
    ]
  },
  {
    id: 'all-metrics',
    name: 'Alle Metriken',
    description: 'Übersicht aller verfügbaren Metriken',
    icon: 'pi pi-th-large',
    category: 'overview',
    charts: [
      {
        title: 'Wärmepumpe Temperaturen',
        queries: [
          { label: 'Aussen', query: 'idm_heatpump_temp_outside', color: '#3b82f6' },
          { label: 'Vorlauf', query: 'idm_heatpump_temp_heat_pump_flow', color: '#ef4444' },
          { label: 'Rücklauf', query: 'idm_heatpump_temp_heat_pump_return', color: '#f59e0b' }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Warmwasser Temperaturen',
        queries: [
          { label: 'WW oben', query: 'idm_heatpump_temp_water_heater_top', color: '#ef4444' },
          { label: 'WW unten', query: 'idm_heatpump_temp_water_heater_bottom', color: '#f59e0b' }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'Leistung',
        queries: [
          {
            label: 'Leistungsaufnahme',
            query: 'idm_heatpump_power_current_draw',
            color: '#ef4444'
          },
          { label: 'Wärmeleistung', query: 'idm_heatpump_power_current', color: '#3b82f6' }
        ],
        hours: 24,
        yAxisMode: 'dual'
      },
      {
        title: 'Energie',
        queries: [
          { label: 'Gesamt', query: 'idm_heatpump_energy_heat_total', color: '#3b82f6' },
          { label: 'Heizung', query: 'idm_heatpump_energy_heat_heating', color: '#22c55e' },
          { label: 'Warmwasser', query: 'idm_heatpump_energy_heat_total_water', color: '#f59e0b' }
        ],
        hours: 24,
        yAxisMode: 'single'
      },
      {
        title: 'COP',
        queries: [
          {
            label: 'COP',
            query: 'idm_heatpump_power_current / idm_heatpump_power_current_draw',
            color: '#22c55e'
          }
        ],
        hours: 24,
        yAxisMode: 'single'
      }
    ]
  }
]

/**
 * Get template by ID
 */
export function getTemplateById(id) {
  return chartTemplates.find((t) => t.id === id)
}

/**
 * Get templates by category
 */
export function getTemplatesByCategory(category) {
  return chartTemplates.filter((t) => t.category === category)
}

/**
 * Get all categories
 */
export function getCategories() {
  const categories = new Set(chartTemplates.map((t) => t.category))
  return Array.from(categories).map((cat) => ({
    id: cat,
    name: cat.charAt(0).toUpperCase() + cat.slice(1),
    icon: chartTemplates.find((t) => t.category === cat)?.icon || 'pi pi-folder'
  }))
}

export default chartTemplates
