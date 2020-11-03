<template>
    <div id="con">
        <div class="mycontent">
            <h2>Vision Space의 서비스는 간단한 회원가입을 통해 사용가능합니다.</h2>
            <h4>회원이시라면 로그인해주세요</h4>
            <router-link :to="{ 'name':'SignupForm' }">Login/Signup</router-link>
        </div>
    </div>
</template>


<script>

export default{
    name: 'LoginPlz',
    methods: {
        movingBackground() {
            let con = document.querySelector('#con');
            window.onmousemove = function(e){
                let x = - e.clientX/20,
                    y = - e.clientY/20;
                con.style.backgroundPositionX = x + 'px';
                con.style.backgroundPositionY = y + 'px';
            }            
        }
    },
    mounted(){
        document.documentElement.scrollTop = 0;
        this.movingBackground();
    }
}
</script>

<style scoped>
/* body{
    background: linear-gradient(45deg, #8500ff, #5acaff);
    height: 100vh;
} */
#con{
    position: absolute;
    /* top: 5%;
    left: 5%;
    right: 5%;
    bottom: 5%; */
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: url('../assets/space.jpg') #151729;
    box-shadow: 0 15px 30px rgba(0, 0, 0, .5);
    z-index: 10000;
}
#con .mycontent{
    max-width: 600px;
    text-align: center;
}
#con .mycontent h2{
    font-size: 40px;
    color: #fff;
    line-height: 1em;
    margin-bottom: 20px;
}
#con .mycontent h4{
    position: relative;
    font-size: 1.5em;
    margin-bottom: 20px;
    color: #111;
    background: #fff;
    font-weight: 300;
    padding: 10px 20px;
    display: inline-block;
}
#con .mycontent p{
    color: #fff;
    font-size: 1.2em;
}
#con .mycontent a{
    position: relative;
    display: block;
    padding: 10px 25px;
    background: #ff0562;
    color: #fff;
    text-decoration: none;
    margin-top: 25px;
    border-radius: 25px;
    border-bottom: 4px solid #d00d56;
    margin-left: auto;
    margin-right: auto;
    width: 180px;
}
</style>
