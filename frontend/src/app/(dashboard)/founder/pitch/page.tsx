'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import styles from './PitchPractice.module.css';

interface Message {
  id: string;
  sender: 'ai' | 'user';
  senderLabel: string;
  text: string;
}

export default function PitchPracticePage() {
  const router = useRouter();
  const [persona, setPersona] = useState('Seed-stage fintech investor');
  const [startup, setStartup] = useState('Your startup');
  const [inputText, setInputText] = useState('');

  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'ai',
      senderLabel: 'AI Investor',
      text: 'Hi — I invest in early-stage fintech. Can you walk me through your startup in 30 seconds?',
    },
    {
      id: '2',
      sender: 'user',
      senderLabel: 'You',
      text: 'We help solo founders automate tax compliance so they can focus on growth instead of paperwork.',
    },
    {
      id: '3',
      sender: 'ai',
      senderLabel: 'AI Investor',
      text: 'That sounds familiar. What makes your solution defensible, and how do you plan to acquire users at scale?',
    },
    {
      id: '4',
      sender: 'user',
      senderLabel: 'You',
      text: 'We integrate directly with accounting tools founders already use, and our first cohort retained 85% month over month.',
    },
    {
      id: '5',
      sender: 'ai',
      senderLabel: 'AI Investor',
      text: 'Retention is strong, but how do you plan to move from a small pilot to a larger market?',
    },
    {
      id: '6',
      sender: 'user',
      senderLabel: 'You',
      text: "We're building a referral loop inside the product, then expanding through partnerships with bookkeeping networks.",
    },
  ]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMsg: Message = {
      id: String(Date.now()),
      sender: 'user',
      senderLabel: 'You',
      text: inputText.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');

    // Simulate investor reply
    setTimeout(() => {
      const aiMsg: Message = {
        id: String(Date.now() + 1),
        sender: 'ai',
        senderLabel: 'AI Investor',
        text: 'Interesting angle. What are your CAC assumptions for those bookkeeping partnerships, and what does the payback period look like in Lahore?',
      };
      setMessages((prev) => [...prev, aiMsg]);
    }, 800);
  };

  const handleEndSession = () => {
    router.push('/founder/feedback');
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Pitch practice"
        subtitle="Practice your investor pitch with a simulated conversation and live rubric feedback."
      />

      {/* Selectors Bar */}
      <div className={styles.selectorBar}>
        <div className={styles.dropdownGroup}>
          <div className={styles.selectBox}>
            <span className={styles.selectLabel}>Investor persona</span>
            <select
              value={persona}
              onChange={(e) => setPersona(e.target.value)}
              style={{
                padding: '6px 12px',
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--font-size-xs)',
                backgroundColor: '#ffffff',
              }}
            >
              <option value="Seed-stage fintech investor">Seed-stage fintech investor</option>
              <option value="Angel investor (B2B SaaS)">Angel investor (B2B SaaS)</option>
              <option value="Growth VC investor">Growth VC investor</option>
            </select>
          </div>

          <div className={styles.selectBox}>
            <span className={styles.selectLabel}>Startup</span>
            <select
              value={startup}
              onChange={(e) => setStartup(e.target.value)}
              style={{
                padding: '6px 12px',
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--font-size-xs)',
                backgroundColor: '#ffffff',
              }}
            >
              <option value="Your startup">Your startup</option>
              <option value="Munshi Books">Munshi Books</option>
            </select>
          </div>
        </div>

        <div className={styles.disclaimerText}>You are talking to an AI, not a human.</div>
      </div>

      <div className={styles.mainLayout}>
        {/* Left: Practice chat */}
        <div className={styles.chatCard}>
          <div className={styles.chatHeader}>
            <span className={styles.chatTitle}>Practice chat</span>
            <span className={styles.mobileTimerText}>3 min left</span>
          </div>

          <div className={styles.chatMessages}>
            {messages.map((m) => (
              <div
                key={m.id}
                className={m.sender === 'ai' ? styles.messageWrapperAi : styles.messageWrapperUser}
              >
                <span className={styles.senderLabel}>{m.senderLabel}</span>
                <div className={m.sender === 'ai' ? styles.bubbleAi : styles.bubbleUser}>
                  {m.text}
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleSend} className={styles.inputBar}>
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your next response..."
              className={styles.chatInput}
            />
            <Button type="submit" variant="primary">
              Send
            </Button>
            <Button type="button" variant="secondary" onClick={handleEndSession}>
              End session
            </Button>
          </form>
        </div>

        {/* Right: Rubric & Session timer */}
        <div className={styles.rightCol}>
          <div className={styles.rubricCard}>
            <div className={styles.rubricTitle}>Rubric</div>

            <div className={styles.rubricItem}>
              <div className={styles.rubricRow}>
                <span>Clarity</span>
                <span>4 / 5</span>
              </div>
              <div className={styles.rubricTrack}>
                <div className={styles.rubricBar} style={{ width: '80%' }} />
              </div>
            </div>

            <div className={styles.rubricItem}>
              <div className={styles.rubricRow}>
                <span>Market understanding</span>
                <span>3 / 5</span>
              </div>
              <div className={styles.rubricTrack}>
                <div className={styles.rubricBar} style={{ width: '60%' }} />
              </div>
            </div>

            <div className={styles.rubricItem}>
              <div className={styles.rubricRow}>
                <span>Defensibility of numbers</span>
                <span>3 / 5</span>
              </div>
              <div className={styles.rubricTrack}>
                <div className={styles.rubricBar} style={{ width: '60%' }} />
              </div>
            </div>

            <div className={styles.rubricItem}>
              <div className={styles.rubricRow}>
                <span>Handling pushback</span>
                <span>2 / 5</span>
              </div>
              <div className={styles.rubricTrack}>
                <div className={styles.rubricBar} style={{ width: '40%' }} />
              </div>
            </div>
          </div>

          <div className={styles.timerCard}>
            <div className={styles.timerTitle}>Session timer</div>
            <div className={styles.timerValue}>3 min left</div>
          </div>
        </div>
      </div>
    </div>
  );
}
