//登录规则

//邮箱判断规则
export const isEmail=(email:string)=>{
    let reg=/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return reg.test(email);
}

//密码判断规则(8-16位，字母+数字)
export const isPassword=(password:string)=>{
    let reg=/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/;
    return reg.test(password);
}

//6位验证码
export const isVerifyCode=(verifyCode:string)=>{
    let reg=/^\d{6}$/;
    return reg.test(verifyCode)
}

