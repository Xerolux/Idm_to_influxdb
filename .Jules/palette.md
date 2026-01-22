## 2024-05-22 - Accessibility in Vue Modals
**Learning:** Manually built modals in Vue often miss basic accessibility associations that component libraries handle automatically. In `Alerts.vue`, form labels were not associated with inputs, and icon-only buttons lacked aria-labels.
**Action:** Always check manually implemented forms and interactive elements for explicit `for`/`id` associations and `aria-label` attributes, especially when they are outside the primary UI library's scope.

## 2026-01-22 - Inline Validation Accessibility
**Learning:** Inline form validation often visually communicates errors (red text) without programmatic association. In `Login.vue`, the error message was visible but not linked to the input via `aria-describedby` or flagged with `aria-invalid`.
**Action:** When implementing custom validation, always bind `aria-invalid` to the error state and use `aria-describedby` to point to the error message ID. Ensure the error message has `role="alert"` for immediate announcement.
