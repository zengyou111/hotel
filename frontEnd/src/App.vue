<template>
    <div class="container">
        <Top v-if="$route.meta.requireTopAndFooter"/>
        <div class="content">
            <router-view></router-view>
        </div>
        <Bottom v-if="$route.meta.requireTopAndFooter"/>
    </div>
</template>

<script setup lang="ts">



</script>



<style scoped lang="scss">
.container{
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    min-width: 100vw;
    .content{
        justify-content: space-between; /* 将内容区域和底部分开 */
        width: 100vw;
        flex:1;
        .Bottom{
            margin-top: auto;
        }
    }

}

</style>
