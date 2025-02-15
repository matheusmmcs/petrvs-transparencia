<script setup>
const footer = import.meta.env.VITE_FOOTER_TEXT || 'Transparência PGD - 2025';
</script>

<template>
    <div class="layout-footer">{{ footer }}</div>
</template>
