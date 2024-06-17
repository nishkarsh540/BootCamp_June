<template>
    <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="loginUser">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <div v-if="errorMessage" class="error-message">
            {{  errorMessage }}
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            username:'',
            password:'',
            errorMessage:''
        };
    },
    methods:{
        async loginUser(){
            try{
                const response = await axios.post('http://127.0.0.1:5000/api/login',{
                    username:this.username,
                    password: this.password
                });
                const {access_token, user} = response.data;
                localStorage.setItem('token',access_token)
                localStorage.setItem('user',JSON.stringify(user));

                if (user.role == 'admin'){
                    this.$router.push('/admindashboard')
                } else if (user.role == 'store_manager'){
                    this.$router.push('/storedashboard')
                } else {
                    this.$router.push('/userdashboard')
                }
            } catch(error){
                if(error.response && error.response.status === 401){
                    this.errorMessage = 'Invalid Username or PASSWORD'
                } else {
                    this.errorMessage='Login Failed'
                }
            }
        }
    }
};
</script>

<style scoped>
.login-container{
    max-width: 350px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #0d0d0d;
    background-color: antiquewhite;
}
.form-group{
    margin:15px;
}
.form-group label{
    display: block;
    margin-bottom: 5px;
}
.form-group input{
    width: 100%;
    padding:8px;
    box-sizing:border-box;
}
button{
    width:100%;
    padding:10px;
    background-color: aqua;
    border:#0d0d0d;
    border-radius: 20px;
    cursor: pointer;
}
</style>