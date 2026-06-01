// app/page.tsx
'use client';

import React, { useState, useEffect } from 'react';

export default function Home() {
  // Navigation Flow States: 'SETUP' | 'INTERVIEW' | 'REPORT'
  const [screen, setScreen] = useState<'SETUP' | 'INTERVIEW' | 'REPORT'>('SETUP');
  
  // Data State Arrays
  const [interviewId, setInterviewId] = useState('');
  const [resumeText, setResumeText] = useState('');
  const [jdText, setJdText] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState<any>(null);
  const [answerText, setAnswerText] = useState('');
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Strict FSM Question Timer Constraint
  const [timeLeft, setTimeLeft] = useState(60);

  useEffect(() => {
    if (screen !== 'INTERVIEW' || timeLeft <= 0) return;
    const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
    return () => clearTimeout(timer);
  }, [timeLeft, screen]);

  // 1. Initialize Interview Session Node
  const handleStartInterview = async () => {
    if (!resumeText || !jdText) return alert('Please provide both Resume and JD contexts.');
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/interviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText }),
      });
      const data = await res.json();
      setInterviewId(data.interview_id);
      await fetchNextQuestion(data.interview_id);
    } catch (err) {
      alert('Failed to initialize session. Make sure your FastAPI backend is running!');
    } finally {
      setLoading(false);
    }
  };

  // 2. Fetch Active FSM Question Node
  const fetchNextQuestion = async (id: string) => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/interviews/${id}/next-question`, { method: 'POST' });
      const question = await res.json();
      setCurrentQuestion(question);
      setAnswerText('');
      setTimeLeft(60); // Reset countdown clock boundaries
      setScreen('INTERVIEW');
    } catch (err) {
      alert('Error fetching next question.');
    } finally {
      setLoading(false);
    }
  };

  // 3. Submit Response Transaction Edge
  const handleSubmitAnswer = async () => {
    if (!answerText && timeLeft > 0) return alert('Please type an answer or wait for timeout.');
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/interviews/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          interview_id: interviewId,
          answer_text: answerText || '[No response provided - Timeout]',
          response_time_seconds: 60 - timeLeft,
        }),
      });
      const updatedState = await res.json();
      
      if (updatedState.status === 'TERMINATED' || updatedState.status === 'COMPLETED') {
        await fetchFinalReport();
      } else {
        await fetchNextQuestion(interviewId);
      }
    } catch (err) {
      alert('Error submitting response.');
    } finally {
      setLoading(false);
    }
  };

  // 4. Fetch Metric Scorecard Node
  const fetchFinalReport = async () => {
    try {
      const res = await fetch(`http://localhost:8000/interviews/${interviewId}/report`);
      const reportData = await res.json();
      setReport(reportData);
      setScreen('REPORT');
    } catch (err) {
      alert('Error rendering scorecard generation profiles.');
    }
  };

  return (
    <main className="min-h-screen bg-slate-900 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-slate-800 border border-slate-700 rounded-xl p-8 shadow-2xl">
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500 mb-6 text-center">
          PSY AI MOCK INTERVIEW PLATFORM
        </h1>

        {/* SCREEN 1: PROFILE SETUP INGESTION */}
        {screen === 'SETUP' && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-semibold mb-2 text-teal-400">Candidate Resume</label>
              <textarea
                className="w-full h-32 p-3 bg-slate-900 border border-slate-700 rounded-lg focus:outline-none focus:border-teal-500 font-mono text-sm"
                placeholder="Paste Candidate Resume plain text profile here..."
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2 text-blue-400">Target Job Description (JD)</label>
              <textarea
                className="w-full h-32 p-3 bg-slate-900 border border-slate-700 rounded-lg focus:outline-none focus:border-blue-500 font-mono text-sm"
                placeholder="Paste Target Job Description requirements profile here..."
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
              />
            </div>
            <button
              onClick={handleStartInterview}
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-teal-500 to-blue-600 hover:from-teal-400 hover:to-blue-500 font-bold rounded-lg transition shadow-lg disabled:opacity-50"
            >
              {loading ? 'Processing Profiles...' : 'Initialize Interview Session'}
            </button>
          </div>
        )}

        {/* SCREEN 2: ACTIVE RECURSIVE INTERVIEW ENGINE */}
        {screen === 'INTERVIEW' && currentQuestion && (
          <div className="space-y-6">
            <div className="flex justify-between items-center border-b border-slate-700 pb-4">
              <span className="px-3 py-1 bg-slate-700 text-xs rounded-full uppercase font-bold text-teal-400">
                Evaluating Module: {currentQuestion.skill}
              </span>
              <span className={`text-lg font-mono font-bold ${timeLeft < 15 ? 'text-red-400 animate-pulse' : 'text-amber-400'}`}>
                Time Remaining: {timeLeft}s
              </span>
            </div>
            
            <div className="bg-slate-900 border-l-4 border-teal-500 p-4 rounded-r-lg font-medium text-lg italic">
              "{currentQuestion.question_text}"
            </div>

            <div>
              <label className="block text-sm font-semibold mb-2 text-slate-400">Your Response Input</label>
              <textarea
                className="w-full h-40 p-3 bg-slate-900 border border-slate-700 rounded-lg focus:outline-none focus:border-teal-500 text-sm"
                placeholder="Type your objective engineering answer context here..."
                value={answerText}
                onChange={(e) => setAnswerText(e.target.value)}
              />
            </div>

            <button
              onClick={handleSubmitAnswer}
              disabled={loading}
              className="w-full py-4 bg-teal-600 hover:bg-teal-500 font-bold rounded-lg transition"
            >
              {loading ? 'AI Grading Calculation Transpiling...' : 'Submit Response Answer'}
            </button>
          </div>
        )}

        {/* SCREEN 3: ANALYTICS REPORT SCORECARD */}
        {screen === 'REPORT' && report && (
          <div className="space-y-6">
            <div className="text-center border-b border-slate-700 pb-6">
              <h2 className="text-2xl font-bold text-teal-400">Session Evaluation Blueprint Complete</h2>
              <p className="text-sm text-slate-400 mt-1">FSM Audit Trail Process Session Successfully Parsed</p>
            </div>

            <div className="grid grid-cols-2 gap-4 text-center">
              <div className="bg-slate-900 p-4 border border-slate-700 rounded-lg">
                <div className="text-xs text-slate-400 uppercase font-bold">Readiness Score</div>
                <div className="text-4xl font-extrabold text-teal-400 mt-1">{report.readiness.readiness_score}/100</div>
              </div>
              <div className="bg-slate-900 p-4 border border-slate-700 rounded-lg flex flex-col justify-center">
                <div className="text-xs text-slate-400 uppercase font-bold">Hiring Indicator</div>
                <div className="text-2xl font-bold text-blue-400 mt-1">{report.hiring_recommendation}</div>
              </div>
            </div>

            <div className="space-y-3">
              <h3 className="text-lg font-bold border-b border-slate-700 pb-1 text-slate-300">Category Metric Breakdowns</h3>
              <div>
                <div className="flex justify-between text-xs mb-1"><span>Technical Insight Execution</span><span>{report.readiness.technical_score}%</span></div>
                <div className="w-full h-2 bg-slate-900 rounded-full"><div className="h-2 bg-teal-500 rounded-full" style={{ width: `${report.readiness.technical_score}%` }}></div></div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1"><span>Communication & Clarity</span><span>{report.readiness.communication_score}%</span></div>
                <div className="w-full h-2 bg-slate-900 rounded-full"><div className="h-2 bg-blue-500 rounded-full" style={{ width: `${report.readiness.communication_score}%` }}></div></div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-900/50 p-4 border border-red-900/50 rounded-lg">
                <h4 className="text-sm font-bold text-red-400 uppercase mb-2">Core Areas of Opportunity</h4>
                <ul className="text-xs list-disc pl-4 space-y-1 text-slate-300">
                  {report.weaknesses.map((w: string, i: number) => <li key={i}>{w}</li>)}
                </ul>
              </div>
              <div className="bg-slate-900/50 p-4 border border-emerald-900/50 rounded-lg">
                <h4 className="text-sm font-bold text-emerald-400 uppercase mb-2">Observed Strengths</h4>
                <ul className="text-xs list-disc pl-4 space-y-1 text-slate-300">
                  {report.strengths.map((s: string, i: number) => <li key={i}>{s}</li>)}
                </ul>
              </div>
            </div>

            <button
              onClick={() => setScreen('SETUP')}
              className="w-full py-3 bg-slate-700 hover:bg-slate-600 font-bold rounded-lg transition text-sm"
            >
              Initialize New Interview Profile Session
            </button>
          </div>
        )}
      </div>
    </main>
  );
}