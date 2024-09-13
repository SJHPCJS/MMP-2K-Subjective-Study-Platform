<template>
  <el-container>
    <el-header>
      <div>Macro Photography IQA</div>
      <div>{{ userId }}</div>
    </el-header>
    <el-main>
      <div class="content-wrapper">
        <h1 class="before-start">Before start...</h1>
        <div class="text-container">
          <p class="intro-text">
            We want to recall that this IQA task only focuses on the
            <span class="highlight">technical quality</span>
            of the images.
          </p>
        </div>
        <div class="button-container">
          <el-button type="primary" round @click="goToTrainPage">Go to training!</el-button>
          <el-button type="primary" round @click="goToMenuPage">Skip the training</el-button>
        </div>
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
    goToTrainPage() {
      this.$router.push({ name: 'TrainPage', params: { id: this.userId } });
    },
    goToMenuPage() {
      this.$router.push({ name: 'MenuPage', params: { id: this.userId } });
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

.el-main {
  background-color: #E9EEF3;
  color: #333;
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 60px);
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.before-start {
  font-size: 32px;
  margin-bottom: 20px;
}

.text-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.intro-text {
  font-size: 28px;
  line-height: 1.5;
  color: #333;
}

.highlight {
  color: red;
  font-weight: bold;
}

.button-container {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-top: 20px;
}
</style>
