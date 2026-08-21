import React, { useState } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Auth from './pages/Auth';

function LandingPage() {
  const navigate = useNavigate();
  
  const handleGetStarted = () => {
    navigate('/compare');
  };
  return (
    <div className="min-h-screen flex flex-col">
      {/* TopNavBar */}
      <header className="bg-white fixed top-0 w-full z-50 flex justify-between items-center px-6 h-16 border-b border-outline-variant shadow-sm">
        <div className="flex items-center gap-6">
          <a className="text-[21px] font-extrabold text-primary tracking-tight" href="#">CompareX</a>
        </div>
        <nav className="hidden md:flex items-center gap-6">
          <a className="text-[16px] text-primary font-bold border-b-2 border-primary pb-1 mt-1 hover:text-primary transition-colors" href="#">Home</a>
          <a className="text-[16px] text-on-surface-variant hover:text-primary transition-colors" href="#features">Features</a>
        </nav>
        <div className="flex items-center gap-3">
          <button onClick={() => navigate('/auth', { state: { isLogin: true } })} className="hidden md:inline-flex items-center justify-center bg-surface-container-low text-on-surface hover:bg-surface-variant px-3 py-1.5 rounded-full text-[14px] font-bold transition-colors">Log In</button>
          <button onClick={() => navigate('/auth', { state: { isLogin: false } })} className="inline-flex items-center justify-center bg-on-secondary-fixed text-on-primary hover:-translate-y-px px-6 py-1.5 rounded-full text-[14px] font-bold transition-transform shadow-sm">Sign Up</button>
        </div>
      </header>

      <main className="flex-grow pt-16">
        {/* Hero Section */}
        <section className="relative pt-[72px] pb-12 px-6 overflow-hidden hero-glow">
          <div className="max-w-[1040px] mx-auto text-center relative z-10">
            <h1 className="text-[38px] md:text-[58px] font-extrabold text-on-surface mb-6 max-w-3xl mx-auto tracking-tight leading-[1.08]" style={{ letterSpacing: '-2px' }}>Decide with Confidence</h1>
            <p className="text-[18px] text-on-surface-variant max-w-2xl mx-auto mb-[34px] font-normal leading-[1.35]" style={{ letterSpacing: '-0.2px' }}>Harness the power of intelligent side-by-side comparisons. Real-time data, clear specifications, and seamless visual alignment.</p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <button onClick={handleGetStarted} className="w-full sm:w-auto inline-flex items-center justify-center bg-on-secondary-fixed text-on-primary hover:-translate-y-px px-[34px] py-3 rounded-full text-[14px] font-bold transition-all ambient-shadow text-lg">
                Get Started Free
              </button>
            </div>
          </div>

          {/* Browser Mockup */}
          <div className="max-w-[1040px] mx-auto mt-[72px] relative z-10 px-2">
            <div className="bg-white rounded-xl border border-outline-variant ambient-shadow overflow-hidden ai-top-accent">
              {/* Fake Top Bar */}
              <div className="bg-surface-container-low border-b border-outline-variant px-3 py-2 flex items-center gap-2">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-outline-variant"></div>
                  <div className="w-3 h-3 rounded-full bg-outline-variant"></div>
                  <div className="w-3 h-3 rounded-full bg-outline-variant"></div>
                </div>
                <div className="bg-white border border-outline-variant rounded-md px-2 py-1 flex-grow max-w-sm mx-auto flex items-center text-on-surface-variant text-xs font-medium justify-center">
                  <span className="material-symbols-outlined text-[14px] mr-1">lock</span>
                  comparex.app/compare/flagships
                </div>
              </div>
              {/* Fake Content */}
              <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6 bg-background">
                {/* Card 1 */}
                <div className="bg-white rounded-lg border border-outline-variant p-3 atmospheric-shadow">
                  <div className="h-32 bg-surface-container-low rounded-md mb-3 flex items-center justify-center relative overflow-hidden" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAOAhzm1I0hNqcVWFsEJRJxA-Zy0r2_didTnU-Ay3CSFG3pxeLVa5tCLbN3bQo9pDoP4J-4w9pw1MbTWk1N2V9nHO3EP_Cc7PI4vSXSqWjvjglkuS9a9XFHw18U48kRpkwMKbOsiC9Igz1lM-8rFluNNI6pcqZuU1pAiw9iFA2jozzmusxvvjgthdnwRBQb9jTkJhNjSHR9k5JFq4smHZb0VcmRQYREwnfcE_Y6966rbMu0n89lSYro')", backgroundSize: 'cover', backgroundPosition: 'center' }}></div>
                  <h4 className="text-[14px] font-bold text-on-surface mb-1">iPhone 15 Pro</h4>
                  <p className="text-[13px] text-primary font-semibold mb-3">₹1,34,900</p>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center py-2 border-b border-surface-container-high">
                      <span className="text-xs text-on-surface-variant font-medium">Processor</span>
                      <span className="text-xs text-on-surface font-bold">A16 Bionic</span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-surface-container-high">
                      <span className="text-xs text-on-surface-variant font-medium">Display</span>
                      <span className="text-xs text-on-surface font-bold">6.1" OLED</span>
                    </div>
                  </div>
                </div>
                {/* Card 2 */}
                <div className="bg-white rounded-lg border border-outline-variant p-3 atmospheric-shadow">
                  <div className="h-32 bg-surface-container-low rounded-md mb-3 flex items-center justify-center relative overflow-hidden" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuDofblXFGOrSrPAl7zSE7-T-ROc9Kt0RFKOHmWHHgkqBnVt9Z8cPIW6xNQ0VymhoYjMaFq_tH0QmUERhj69FNJz6IdgKidMOZVi-PsGBQP6dnNceYOkdqyst2jrjmjUUlzLtWx8-Tin1p7EQZEgelhTlnkR7Sa3kUtFXtbwM2UMCMZUlLfGc7284b1mldIdikTR9fERwlSUmKn3t0vL7W5ia3V-N58C76YqfHfjgHt0nTNTjVSyCYeS')", backgroundSize: 'cover', backgroundPosition: 'center' }}></div>
                  <h4 className="text-[14px] font-bold text-on-surface mb-1">Samsung Galaxy S24 Ultra</h4>
                  <p className="text-[13px] text-primary font-semibold mb-3">₹1,29,999</p>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center py-2 border-b border-surface-container-high">
                      <span className="text-xs text-on-surface-variant font-medium">Processor</span>
                      <span className="text-xs text-on-surface font-bold">Snapdragon 8</span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-surface-container-high">
                      <span className="text-xs text-on-surface-variant font-medium">Display</span>
                      <span className="text-xs text-on-surface font-bold">6.2" AMOLED</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>




        {/* Features Section */}
        <section id="features" className="py-12 px-6 bg-background">
          <div className="max-w-[1040px] mx-auto">
            <div className="text-center mb-[34px]">
              <h2 className="text-[25px] font-bold text-on-surface mb-2 leading-[1.25]" style={{ letterSpacing: '-0.5px' }}>Clarity in Every Detail</h2>
              <p className="text-[16px] text-on-surface-variant max-w-2xl mx-auto leading-[1.7]">Stop juggling tabs. Our comparison engine brings everything into one unified, legible view.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Feature 1 */}
              <div className="bg-white p-6 rounded-xl border border-outline-variant atmospheric-shadow group hover:border-primary transition-colors">
                <div className="w-12 h-12 rounded-lg bg-surface-container-low flex items-center justify-center mb-3 group-hover:bg-primary-container transition-colors">
                  <span className="material-symbols-outlined text-primary group-hover:text-on-primary-container">tune</span>
                </div>
                <h3 className="text-[14px] font-semibold text-on-surface mb-2 leading-[1.5]" style={{ letterSpacing: '-0.01em' }}>Real-time Specs</h3>
                <p className="text-[13px] text-on-surface-variant leading-[1.65]">Access the latest hardware and software specifications pulled directly from verified manufacturer databases.</p>
              </div>
              {/* Feature 2 */}
              <div className="bg-white p-6 rounded-xl border border-outline-variant atmospheric-shadow group hover:border-primary transition-colors">
                <div className="w-12 h-12 rounded-lg bg-surface-container-low flex items-center justify-center mb-3 group-hover:bg-primary-container transition-colors">
                  <span className="material-symbols-outlined text-primary group-hover:text-on-primary-container">monitoring</span>
                </div>
                <h3 className="text-[14px] font-semibold text-on-surface mb-2 leading-[1.5]" style={{ letterSpacing: '-0.01em' }}>Price Tracking</h3>
                <p className="text-[13px] text-on-surface-variant leading-[1.65]">Monitor historical price drops and current availability across major retailers instantly.</p>
              </div>
              {/* Feature 3 */}
              <div className="bg-white p-6 rounded-xl border border-outline-variant atmospheric-shadow group hover:border-primary transition-colors">
                <div className="w-12 h-12 rounded-lg bg-surface-container-low flex items-center justify-center mb-3 group-hover:bg-primary-container transition-colors">
                  <span className="material-symbols-outlined text-primary group-hover:text-on-primary-container">forum</span>
                </div>
                <h3 className="text-[14px] font-semibold text-on-surface mb-2 leading-[1.5]" style={{ letterSpacing: '-0.01em' }}>User Reviews Integration</h3>
                <p className="text-[13px] text-on-surface-variant leading-[1.65]">Aggregate sentiment and critical feedback from verified buyers directly alongside the spec sheet.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section id="cta" className="py-12 px-6 bg-surface-container-low border-t border-outline-variant relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary rounded-full mix-blend-multiply blur-3xl opacity-10 translate-x-1/2 -translate-y-1/2"></div>
          <div className="max-w-3xl mx-auto text-center relative z-10 spine-accent pl-6 pr-6 py-3 bg-white rounded-xl border border-outline-variant atmospheric-shadow">
            <h2 className="text-[21px] font-bold text-on-surface mb-2 leading-[1.3]" style={{ letterSpacing: '-0.3px' }}>Ready to compare?</h2>
            <p className="text-[16px] text-on-surface-variant mb-6 leading-[1.7]">Create your first list today and make better decisions faster.</p>
            <button onClick={handleGetStarted} className="inline-flex items-center justify-center bg-on-secondary-fixed text-on-primary hover:-translate-y-px px-[34px] py-3 rounded-full text-[14px] font-bold transition-transform shadow-sm">
              Start Comparing Now
              <span className="material-symbols-outlined ml-2 text-[18px]">arrow_forward</span>
            </button>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full py-12 px-6 flex flex-col md:flex-row justify-between items-start max-w-[1040px] mx-auto border-t border-outline-variant bg-surface-container-low text-[13px] text-primary mt-auto">
        <div className="mb-6 md:mb-0">
          <span className="text-[18px] font-bold text-on-surface block mb-2 leading-[1.35]" style={{ letterSpacing: '-0.2px' }}>CompareX</span>
          <p className="text-on-surface-variant">© 2026 CompareX Inc. All rights reserved.</p>
        </div>
        <div className="grid grid-cols-2 gap-[34px]">
          <div className="flex flex-col gap-2">
            <a className="text-on-surface-variant hover:underline decoration-primary" href="#features">Features</a>
            <a className="text-on-surface-variant hover:underline decoration-primary" href="#">Documentation</a>
          </div>
          <div className="flex flex-col gap-2">
            <a className="text-on-surface-variant hover:underline decoration-primary" href="#">Contact Support</a>
            <a className="text-on-surface-variant hover:underline decoration-primary" href="#">Privacy Policy</a>
            <a className="text-on-surface-variant hover:underline decoration-primary" href="#">Terms of Service</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

function MainPage() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showSources, setShowSources] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setShowSources(false);

    try {
      const token = await currentUser.getIdToken();
      const res = await fetch('http://localhost:5000/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        let errorMsg = 'Failed to fetch from server';
        try {
          const errData = await res.json();
          errorMsg = errData.error || errData.detail || errorMsg;
        } catch (e) {
          errorMsg = `Server returned status ${res.status}`;
        }
        throw new Error(errorMsg);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderStars = (rating) => {
    if (!rating) return null;
    const full = Math.floor(rating);
    const half = rating % 1 >= 0.5;
    const stars = [];
    for (let i = 0; i < 5; i++) {
      if (i < full) stars.push(<span key={i} className="material-symbols-outlined text-[16px] text-amber-500" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>);
      else if (i === full && half) stars.push(<span key={i} className="material-symbols-outlined text-[16px] text-amber-500" style={{ fontVariationSettings: "'FILL' 1" }}>star_half</span>);
      else stars.push(<span key={i} className="material-symbols-outlined text-[16px] text-outline-variant">star</span>);
    }
    return stars;
  };

  const formatPrice = (price, currency) => {
    if (!price) return 'Price N/A';
    if (currency === 'INR' || !currency) return `₹${price.toLocaleString('en-IN')}`;
    return `${currency} ${price.toLocaleString()}`;
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="bg-white fixed top-0 w-full z-50 flex justify-between items-center px-6 h-16 border-b border-outline-variant shadow-sm">
        <div className="flex items-center gap-3">
          <button onClick={() => navigate('/')} className="flex items-center gap-2 text-[21px] font-extrabold text-primary tracking-tight hover:opacity-80 transition-opacity">
            <span className="material-symbols-outlined text-[20px]">arrow_back</span>
            CompareX
          </button>
        </div>
        <div className="relative">
          <button 
            onClick={() => setIsProfileOpen(!isProfileOpen)}
            className="w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center border-2 border-transparent hover:border-indigo-600 transition-colors overflow-hidden"
          >
            {currentUser?.photoURL ? (
              <img src={currentUser.photoURL} alt="Profile" className="w-full h-full object-cover" />
            ) : (
              <span className="text-indigo-600 font-bold text-[14px]">
                {currentUser?.displayName ? currentUser.displayName.charAt(0).toUpperCase() : (currentUser?.email ? currentUser.email.charAt(0).toUpperCase() : 'U')}
              </span>
            )}
          </button>

          {isProfileOpen && (
            <>
              <div 
                className="fixed inset-0 z-40"
                onClick={() => setIsProfileOpen(false)}
              ></div>
              <div className="absolute right-0 mt-3 w-[280px] bg-white rounded-xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-gray-100 border-t-[3px] border-t-indigo-600 z-50 p-6 flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-indigo-100 flex items-center justify-center mb-4 overflow-hidden shadow-sm">
                  {currentUser?.photoURL ? (
                    <img src={currentUser.photoURL} alt="Profile" className="w-full h-full object-cover" />
                  ) : (
                    <span className="text-indigo-600 font-bold text-[24px]">
                      {currentUser?.displayName ? currentUser.displayName.charAt(0).toUpperCase() : (currentUser?.email ? currentUser.email.charAt(0).toUpperCase() : 'U')}
                    </span>
                  )}
                </div>
                <h3 className="text-[18px] font-bold text-gray-900 mb-1">{currentUser?.displayName || 'User'}</h3>
                <p className="text-[13px] text-gray-500 mb-6">{currentUser?.email}</p>
                
                <button className="w-full py-2.5 rounded-full border border-gray-200 text-gray-800 font-bold text-[13px] flex items-center justify-center gap-2 hover:bg-gray-50 transition-colors mb-3">
                  <span className="material-symbols-outlined text-[18px]">settings</span>
                  Account Settings
                </button>
                <button 
                  onClick={async () => { await logout(); navigate('/auth'); }}
                  className="w-full py-2.5 rounded-full border border-red-300 text-red-600 font-bold text-[13px] flex items-center justify-center gap-2 hover:bg-red-50 transition-colors"
                >
                  <span className="material-symbols-outlined text-[18px]">logout</span>
                  Sign Out
                </button>
              </div>
            </>
          )}
        </div>
      </header>

      <main className="flex-grow pt-24 pb-12 px-6">
        {/* Search Bar */}
        <section className="max-w-[850px] mx-auto mb-8">
          <form onSubmit={handleSearch} className="flex items-center gap-3 bg-white p-2 rounded-full border border-outline-variant ambient-shadow transition-all focus-within:border-primary">
            <span className="material-symbols-outlined text-on-surface-variant ml-3 text-[22px]">search</span>
            <input
              type="text"
              className="w-full bg-transparent border-none focus:ring-0 px-2 py-2 text-[16px] text-on-surface placeholder:text-on-surface-variant outline-none"
              placeholder="Ask anything... e.g., Best phone under ₹30,000 with good camera"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button
              type="submit"
              disabled={loading}
              className="shrink-0 inline-flex items-center justify-center bg-on-secondary-fixed text-on-primary hover:-translate-y-px px-6 py-2.5 rounded-full text-[14px] font-bold transition-all disabled:opacity-50 gap-2"
            >
              {loading ? (
                <>
                  <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                  Thinking...
                </>
              ) : (
                <>
                  <span className="material-symbols-outlined text-[18px]">auto_awesome</span>
                  Compare
                </>
              )}
            </button>
          </form>
        </section>

        {/* Loading Skeleton */}
        {loading && (
          <div className="max-w-[850px] mx-auto space-y-6 animate-pulse">
            <div className="bg-white rounded-xl border border-outline-variant p-6 ai-top-accent">
              <div className="h-5 w-48 bg-surface-container-highest rounded mb-4"></div>
              <div className="space-y-2">
                <div className="h-4 w-full bg-surface-container-high rounded"></div>
                <div className="h-4 w-5/6 bg-surface-container-high rounded"></div>
                <div className="h-4 w-4/6 bg-surface-container-high rounded"></div>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-xl border border-outline-variant p-5">
                  <div className="h-4 w-20 bg-surface-container-highest rounded-full mb-3"></div>
                  <div className="h-5 w-3/4 bg-surface-container-highest rounded mb-2"></div>
                  <div className="h-6 w-1/3 bg-primary-fixed rounded mb-4"></div>
                  <div className="space-y-2">
                    <div className="h-3 w-full bg-surface-container-high rounded"></div>
                    <div className="h-3 w-full bg-surface-container-high rounded"></div>
                    <div className="h-3 w-full bg-surface-container-high rounded"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="max-w-[850px] mx-auto mb-8">
            <div className="p-4 bg-error-container text-on-error-container rounded-xl flex items-center gap-3">
              <span className="material-symbols-outlined">error</span>
              <div>
                <p className="font-bold text-[14px]">Something went wrong</p>
                <p className="text-[13px]">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="max-w-[1040px] mx-auto">
            <h2 className="text-[28px] font-bold text-gray-900 mb-6">Your CompareX result</h2>

            {/* AI Answer */}
            {result.answer && (
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
                <div className="flex items-start gap-4 mb-4">
                  <div className="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-indigo-600 text-[20px]">auto_awesome</span>
                  </div>
                  <div>
                    <div className="text-[11px] font-extrabold uppercase tracking-[0.1em] text-indigo-600 mb-0.5">AI ANALYSIS</div>
                    <h3 className="text-[20px] font-bold text-gray-900 leading-none">AI Answer</h3>
                  </div>
                </div>
                <div className="text-[15px] text-gray-700 whitespace-pre-wrap leading-[1.75]">{result.answer}</div>
              </div>
            )}

            {/* Products Grid */}
            {result.products && result.products.length > 0 && (
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
                <div className="flex items-start gap-4 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-emerald-600 text-[20px]">grid_on</span>
                  </div>
                  <div>
                    <div className="text-[11px] font-extrabold uppercase tracking-[0.1em] text-indigo-600 mb-0.5">MATCHED PRODUCTS</div>
                    <h3 className="text-[20px] font-bold text-gray-900 leading-none">Relevant Products</h3>
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                  {result.products.map((product, idx) => (
                    <div key={idx} className="bg-white rounded-xl border border-gray-200 p-5 flex flex-col justify-between">
                      <h4 className="text-[15px] font-bold text-gray-900 mb-5 leading-snug">{product.name}</h4>
                      
                      <div className="space-y-0">
                        <div className="border-t border-gray-100 py-3 flex gap-2">
                          <span className="text-[13px] text-gray-500">Brand:</span>
                          <span className="text-[13px] text-gray-800">{product.brand || 'N/A'}</span>
                        </div>
                        <div className="border-t border-gray-100 py-3 flex gap-2">
                          <span className="text-[13px] text-gray-500">Price:</span>
                          <span className="text-[13px] text-gray-800">{formatPrice(product.price, product.currency)}</span>
                        </div>
                        <div className="border-t border-gray-100 py-3 flex gap-2">
                          <span className="text-[13px] text-gray-500">Rating:</span>
                          <span className="text-[13px] text-gray-800">{product.rating || 'N/A'}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Sources / Documents */}
            {result.documents && result.documents.length > 0 && (
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
                <div className="flex items-start gap-4 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-orange-50 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-orange-600 text-[20px]">article</span>
                  </div>
                  <div>
                    <div className="text-[11px] font-extrabold uppercase tracking-[0.1em] text-indigo-600 mb-0.5">SOURCE MATERIAL</div>
                    <h3 className="text-[20px] font-bold text-gray-900 leading-none">Product Documentation</h3>
                  </div>
                </div>
                
                <div className="space-y-4">
                  {result.documents.map((doc, idx) => (
                    <div key={idx} className="bg-white rounded-xl border border-gray-200 overflow-hidden">
                      <div className="border-l-[4px] border-indigo-500 p-5">
                        <div className="mb-3">
                          <span className="inline-flex items-center px-2 py-1 rounded text-[11px] font-extrabold text-indigo-600 bg-indigo-50">
                            Page {doc.page || 'N/A'}
                          </span>
                        </div>
                        <p className="text-[13px] text-gray-600 leading-[1.7]">{doc.text}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Empty State */}
        {!loading && !result && !error && (
          <div className="max-w-[850px] mx-auto text-center pt-16">
            <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-surface-container-low flex items-center justify-center">
              <span className="material-symbols-outlined text-primary text-[40px]">compare_arrows</span>
            </div>
            <h2 className="text-[21px] font-bold text-on-surface mb-2">What would you like to compare?</h2>
            <p className="text-[15px] text-on-surface-variant max-w-md mx-auto mb-8">Ask me anything about products — recommendations, comparisons, specs, or pricing.</p>
            <div className="flex flex-wrap justify-center gap-2">
              {[
                'Best phone under ₹20,000',
                'Compare iPhone 15 vs Samsung S24',
                'Gaming phone with best battery',
                'Phone with best camera under ₹30,000',
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => { setQuery(suggestion); }}
                  className="px-4 py-2 rounded-full border border-outline-variant text-[13px] text-on-surface-variant hover:border-primary hover:text-primary hover:bg-primary-fixed/30 transition-all"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function PrivateRoute({ children }) {
  const { currentUser } = useAuth();
  return currentUser ? children : <Navigate to="/auth" />;
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/auth" element={<Auth />} />
      <Route path="/compare" element={
        <PrivateRoute>
          <MainPage />
        </PrivateRoute>
      } />
    </Routes>
  );
}

export default App;
