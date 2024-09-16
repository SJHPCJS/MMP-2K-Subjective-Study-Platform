<template>
  <el-container>
    <el-header>
      <div>Macro Photography IQA</div>
      <div>{{ userId }}</div>
    </el-header>
    <div class="section-title">{{ capitalizedSectionTitle }}</div>
    <el-main class="main-content">
      <!-- 图片网格 -->
      <div class="image-grid" v-if="images.length > 0">
        <div v-for="(image, index) in images" :key="index" class="image-item">
          <img :src="image" alt="Image" class="image-preview"/>
        </div>
      </div>
    </el-main>
    <el-footer>
      <div class="button-container">
        <el-button type="primary" round @click="goback">Go back</el-button>
        <el-button type="primary" round @click="loadImages('overexposure')">Overexposure</el-button>
        <el-button type="primary" round @click="loadImages('underexposure')">Underexposure</el-button>
        <el-button type="primary" round @click="loadImages('out_of_focus')">Out of Focus</el-button>
        <el-button type="primary" round @click="loadImages('motion_blur')">Motion Blur</el-button>
        <el-button type="primary" round @click="loadImages('noise_and_grainy')">Noisy and Grainy</el-button>
      </div>
    </el-footer>
  </el-container>
</template>

<script>
export default {
  name: 'ReferenceIntro',
  data() {
    return {
      userId: null,
      batch: null,
      images: [],
      sectionTitle: 'Overexposure',
      imagesData: {
        overexposure: [],
        underexposure: [],
        out_of_focus: [],
        motion_blur: [],
        noise_and_grainy: []
      }
    };
  },
  computed: {
    capitalizedSectionTitle() {
      return this.sectionTitle.replace(/\b\w/g, (char) => char.toUpperCase());
    }
  },
  created() {
    this.userId = this.$route.params.id;
    this.batch = this.$route.params.batch;
    this.loadAllImages();
    this.loadImages('overexposure');
  },
  methods: {
    goback() {
      this.$router.push({ name: 'MainPage', params: { id: this.userId, batch: this.batch } });
    },
    loadAllImages() {
      const folders = ['overexposure', 'underexposure', 'out_of_focus', 'motion_blur', 'noise_and_grainy'];
      folders.forEach(folder => {
        const images = [];
        for (let i = 1; i <= 6; i++) {
          const image = require(`@/assets/annotation_examples/${folder}/${i}.jpg`);
          images.push(image);
        }
        this.imagesData[folder] = images;
      });
    },
    loadImages(folder) {
      this.images = this.imagesData[folder];
      this.sectionTitle = folder.replace(/_/g, ' ');
    }
  }
}
</script>

<style scoped>
/* 调整页面布局和样式 */
html, body, #app, .el-container {
  height: 100%;
  margin: 0;
  padding: 0;
}

.el-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.el-header {
  background-color: #143FAE;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 24px;
  padding: 10px;
}

.section-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin: 20px 0;
  text-align: center;
}

.el-main {
  flex: 1;
  background-color: #E9EEF3;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  overflow: hidden; /* 防止滚动 */
}

.image-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  width: 100%;
}

.image-item {
  flex: 1 1 calc(33.333% - 20px);
  max-width: calc(33.333% - 20px);
  box-sizing: border-box;
}

.image-preview {
  width: 100%;
  height: auto;
  max-height: 500px; /* 根据需要调整 */
}

.el-footer {
  background-color: #E9EEF3;
  padding: 10px;
}

.button-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}
</style>
