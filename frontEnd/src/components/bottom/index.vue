<template>
    <footer>
        <div class="footer-content">
            <!-- 版权信息 -->
            <div class="copyright">
                <p>&copy; 2025 酒店管理系统. All rights reserved.</p>
            </div>

            <!-- 导航链接 -->
            <div class="footer-links">
                <a href="#" v-for="link in links" :key="link.text" @click="handleLinkClick(link)">
                    {{ link.text }}
                </a>
            </div>

            <!-- 社交媒体图标 -->
            <div class="social-media">
                <a
                    href="#"
                    v-for="social in socialMedia"
                    :key="social.name"
                    @click="handleSocialClick(social)"
                >
                    <i :class="`icon-${social.icon}`"></i>
                </a>
            </div>

        </div>
    </footer>
</template>

<script setup lang="ts" name="Bottom">
import { ref } from "vue";

// 定义导航链接类型
interface Link {
    text: string;
    url: string;
}

// 定义社交媒体类型
interface SocialMedia {
    name: string;
    icon: string;
    url: string;
}

// 导航链接数据
const links = ref<Link[]>([
    { text: "Privacy Policy", url: "#" },
    { text: "Terms of Service", url: "#" },
    { text: "Contact Us", url: "#" },
]);

// 社交媒体数据
const socialMedia = ref<SocialMedia[]>([
    { name: "WeChat", icon: "wechat", url: "#" },
    { name: "Weibo", icon: "weibo", url: "#" },
    { name: "LinkedIn", icon: "linkedin", url: "#" },
]);

// 处理导航链接点击
const handleLinkClick = (link: Link) => {
    console.log("Clicked link:", link.text);
    // 这里可以添加路由跳转逻辑
};

// 处理社交媒体点击
const handleSocialClick = (social: SocialMedia) => {
    console.log("Clicked social media:", social.name);
    // 这里可以添加跳转到社交媒体页面的逻辑
};


</script>

<style scoped>
    footer {
        background: linear-gradient(180deg, #f5f5f5, #e0e0e0);
        width: 100vw;
        height: 70px;
        margin-bottom: 0px;
        border-top: 2px solid #ddd;
        text-align: center;
    }

    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .copyright p {
        font-size: 14px;
        color: #666;
        margin: 0;
    }

    .footer-links {
        display: flex;
        justify-content: center;
        gap: 20px;
    }

    .footer-links a {
        text-decoration: none;
        color: #333;
        font-size: 14px;
    }

    .footer-links a:hover {
        color: #007aff;
    }

    .social-media {
        display: flex;
        justify-content: center;
        gap: 15px;
    }

    .social-media a {
        color: #333;
        font-size: 18px;
    }

    .social-media a:hover {
        color: #007aff;
    }

    .back-to-top {
        margin-top: 10px;
    }

.back-to-top a {
    text-decoration: none;
    color: #007aff;
    font-size: 14px;
}

.back-to-top a:hover {
    text-decoration: underline;
}
</style>