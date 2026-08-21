import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';

export default function Auth() {
  const location = useLocation();
  const [isLogin, setIsLogin] = useState(location.state?.isLogin ?? true);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const { login, signup, loginWithGoogle, loginWithGithub } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await signup(email, password, name);
      }
      navigate('/compare');
    } catch (err) {
      console.error("🔥 FIREBASE ERROR:", err.code, err.message);
      setError(err.message || 'Failed to authenticate');
    } finally {
      setLoading(false);
    }
  }

  async function handleProviderLogin(provider) {
    setError('');
    setLoading(true);
    try {
      if (provider === 'google') await loginWithGoogle();
      if (provider === 'github') await loginWithGithub();
      navigate('/compare');
    } catch (err) {
      console.error("🔥 FIREBASE ERROR:", err.code, err.message);
      setError(err.message || `Failed to login with ${provider}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4" style={{
      backgroundImage: 'radial-gradient(#e5e7eb 1px, transparent 1px)',
      backgroundSize: '24px 24px'
    }}>
      {/* Logo */}
      <button onClick={() => navigate('/')} className="flex items-center gap-2 text-[22px] font-bold text-indigo-600 mb-8 hover:opacity-80 transition-opacity">
        <span className="material-symbols-outlined text-[20px]">arrow_back</span>
        CompareX
      </button>

      {/* Main Card */}
      <div className="bg-white rounded-xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] w-full max-w-[420px] p-8 border border-gray-100 border-t-[3px] border-t-indigo-600">
        
        <div className="mb-8">
          <h2 className="text-[24px] font-bold text-gray-900 mb-2 tracking-tight">
            {isLogin ? 'Welcome back' : 'Create an account'}
          </h2>
          <p className="text-[14px] text-gray-500">
            {isLogin ? 'Sign in to your account to continue.' : 'Join us to unlock intelligent comparisons.'}
          </p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-3 rounded-lg mb-6 text-[13px] font-medium border border-red-100">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {!isLogin && (
            <div>
              <label className="block text-[13px] font-bold text-gray-800 mb-1.5">Full name</label>
              <input
                type="text"
                required
                className="w-full px-3.5 py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-[2px] focus:ring-indigo-100 focus:border-indigo-500 transition-all text-[14px] text-gray-900"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
              />
            </div>
          )}
          <div>
            <label className="block text-[13px] font-bold text-gray-800 mb-1.5">Email address</label>
            <input
              type="email"
              required
              className="w-full px-3.5 py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-[2px] focus:ring-indigo-100 focus:border-indigo-500 transition-all text-[14px] text-gray-900"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
          </div>
          
          <div>
            <label className="block text-[13px] font-bold text-gray-800 mb-1.5">Password</label>
            <input
              type="password"
              required
              className="w-full px-3.5 py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-[2px] focus:ring-indigo-100 focus:border-indigo-500 transition-all text-[14px] text-gray-900 font-mono tracking-widest"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          {isLogin && (
            <div className="flex items-center gap-2 pt-1">
              <input 
                type="checkbox" 
                id="remember" 
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
              />
              <label htmlFor="remember" className="text-[13px] text-gray-600 cursor-pointer select-none">
                Remember me
              </label>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#4f46e5] text-white font-bold py-2.5 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 mt-2 text-[14px] shadow-sm"
          >
            {isLogin ? 'Sign In' : 'Sign Up'}
          </button>
        </form>

        <div className="mt-8 relative flex items-center justify-center">
          <div className="absolute inset-0 flex items-center w-full">
            <div className="w-full border-t border-gray-200"></div>
          </div>
          <span className="relative px-3 bg-white text-[12px] text-gray-400 font-medium tracking-wide">
            Or continue with
          </span>
        </div>

        <div className="mt-6 flex justify-center">
          <button
            onClick={() => handleProviderLogin('google')}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-white border border-gray-200 text-gray-800 font-bold py-2.5 rounded-lg hover:bg-gray-50 transition-colors text-[13px] shadow-sm"
          >
            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" className="w-4 h-4" />
            Google
          </button>
        </div>
      </div>

      {/* Bottom Link */}
      <div className="mt-8 text-center">
        <span className="text-[13px] text-gray-500">
          {isLogin ? "Don't have an account? " : 'Already have an account? '}
        </span>
        <button
          onClick={() => setIsLogin(!isLogin)}
          className="text-indigo-600 hover:text-indigo-800 text-[13px] font-bold transition-colors"
        >
          {isLogin ? "Sign Up" : 'Sign In'}
        </button>
      </div>
    </div>
  );
}
