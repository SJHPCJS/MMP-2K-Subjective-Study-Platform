<template>
    <div class="background">
        <div class="centered">
            <h1 class="title">Welcome to Subjective Study for<br>Macro Photography IQA!</h1>
            <el-input placeholder="Please enter your ID..." v-model="input" clearable class="half-width input">
            </el-input>
            <el-button type="primary" round class="button" @click="handleSubmit">Start</el-button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { Message } from 'element-ui';

export default {
    name: 'LoginPage',
    data() {
        return {
            input: ''
        }
    },
    methods: {
        async handleSubmit() {
            try {
                const response = await axios.post('http://127.0.0.1:5001/login', { id: this.input });
                if (response.status === 200) {
                    this.goToIntroPage();
                } else {
                    this.showWarning('Record not found');
                }
            } catch (error) {
                if (error.response && error.response.status === 404) {
                    this.showWarning('Record not found');
                } else {
                  this.showWarning('An error occurred');
                }
            }
        },
      goToIntroPage() {
        if (this.$router.currentRoute.name !== 'IntroPage') {
          this.$router.push({name: 'IntroPage', params: {id: this.input}});
        }
      },
      showWarning(message) {
        Message({
          message: message,
          type: 'warning',
          duration: 3000
        });
      }
    }
}
</script>

<style>
.background {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100vh;
  background-image: url('@/assets/background.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  backdrop-filter: blur(10px);
  background-position: center;
}

.title {
  font-size: 4em;
  margin-bottom: 1em;
  text-align: center;
}

.input {
  margin-bottom: 1em;
}

.centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.half-width {
  width: 50%;
}

.background::after {
  content: "";
  background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)),
  url('@/assets/background.jpg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;

  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  position: absolute;
  z-index: -1;
  width: 100%;
  height: 100%;
}
</style>
