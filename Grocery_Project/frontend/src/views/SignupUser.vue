<template>
  <div class="signup-container">
    <h2>SignUp</h2>
    <form @submit.prevent="signupUser">
      <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
          <label for="text">Email:</label>
          <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required>
      </div>
      <div class="form-group">
        <input type="radio" id="user" value="user" v-model="role" required>
        <label for="user">User</label>
        <input type="radio" id="store-manager" value="store-manager" v-model="role" required>
        <label for="store-manager">Store Manager</label>
      </div>
      <button type="submit">Sign Up</button>
    </form>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default{
  data(){
    return{
      username:'',
      email:'',
      password:'',
      role:'user',
      errorMessage:'',
    };
  },
  methods:{
    async signupUser(){
      try{
        await axios.post('http://127.0.0.1:5000/api/signup',{
          username: this.username,
          email: this.email,
          password: this.password,
          role:this.role
        });
        this.$router.push('/login');
      } catch(error){
        this.errorMessage = error.response ? error.response.data.message:'Signup Failed.Please try again'
      }
    }
  }
}


</script>

<style>

</style>