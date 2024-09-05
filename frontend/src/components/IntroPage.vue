<template>
  <el-container>
    <el-header>
      <div>Macro Photography IQA</div>
      <div>{{ userId }}</div>
    </el-header>
    <el-main class="main-content">
      <div class="welcome-container">
        <h1>Welcome {{ userId }}!</h1>
      </div>
      <p class="intro-text">We are conducting an academic study on the perception of the technical quality of macro photography. Your task is to evaluate the quality of macro photography images and identify the factors within the images that influence their overall quality.</p>
      <p class="intro-text"><strong>Introduction</strong><br>This Image Quality Assessment (IQA) specifically focuses on the technical aspects of image quality, emphasizing the evaluation of images based on their technical attributes. In contrast to assessments that consider aesthetic quality and compositional elements, the uniqueness of this study lies in the exclusion of aesthetic judgment and artistic attributes from consideration.</p>
      <div class="button">
        <el-button type="primary" round @click="goToBeforeStartPage">Go!</el-button>
      </div>
    </el-main>
  </el-container>
</template>

<script>
export default {
  created() {
    this.userId = this.$route.params.id;
  },
  data() {
    return {
      userId: null,
    };
  },
  methods: {
    goToBeforeStartPage() {
      this.$router.push({name: 'BeforeStartPage', params: {id: this.userId}});
    }
  }
}
</script>

<style scoped>
.el-header {
  background-color: #143FAE;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 24px;
}

.main-content {
  background-color: #E9EEF3;
  color: #333;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start; /* Align items to the left */
  height: calc(100vh - 60px);
  padding: 0 20%; /* Adjusted padding for wider margins */
  box-sizing: border-box; /* Ensure padding is included in the element's total width and height */
}

.welcome-container {
  width: 100%;
  text-align: center; /* Center the text within the container */
}

.intro-text {
  font-size: 24px;
  line-height: 1.5;
  text-align: left; /* Ensure text is left-aligned */
  color: #333;
}

.button {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  width: 100%;
}
</style>
