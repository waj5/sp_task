<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>登录</h2>
      <el-form
        :model="form"
        :rules="rules"
        ref="loginForm"
        label-width="80px"
        class="login-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">登录</el-button>
          <el-button @click="onReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { login } from "../api/auth"; // 引入登录 API 方法
import { ElMessage } from "element-plus";

export default {
  name: "Login",
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    async onSubmit() {
      // 表单验证
      this.$refs.loginForm.validate(async (valid) => {
        if (valid) {
          try {
            const response = await login(
              this.form.username,
              this.form.password
            );
            ElMessage.success(response.message);
            // 登录成功后的逻辑，比如跳转到首页
            console.log("登录成功", response);
          } catch (error) {
            ElMessage.error(error.response?.data?.detail || "登录失败");
          }
        } else {
          console.log("表单验证失败");
        }
      });
    },
    onReset() {
      this.$refs.loginForm.resetFields();
    },
  },
};
</script>

<style>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f9;
}

.login-card {
  width: 400px;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.login-form {
  margin-top: 20px;
}
</style>
