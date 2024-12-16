import React, { useState } from 'react';
import authService from '../services/authService';

const Auth = () => {
    const [isLogin, setIsLogin] = useState(true); // 切換登入與註冊
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    // 處理表單提交
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            let response;
            if (isLogin) {
                // 登入
                response = await authService.login(email, password);
                setMessage(`Login Successful! Welcome ${response.data.userName}`);
            } else {
                // 註冊
                response = await authService.register(email, password);
                setMessage(`Registration Successful! Welcome ${response.data.userName}`);
            }
        } catch (error) {
            setMessage(error.response?.data?.message || 'An error occurred. Please try again.');
        }
    };

    // 切換登入/註冊模式
    const toggleMode = () => {
        setIsLogin(!isLogin);
        setMessage('');
    };

    return (
        <div className="auth-container">
            <h2>{isLogin ? 'Login' : 'Register'}</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">{isLogin ? 'Login' : 'Register'}</button>
            </form>
            {message && <p className="message">{message}</p>}
            <button className="toggle-button" onClick={toggleMode}>
                {isLogin ? 'Need an account? Register here' : 'Already have an account? Login here'}
            </button>
        </div>
    );
};

export default Auth;
