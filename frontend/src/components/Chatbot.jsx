import { useState } from 'react';
import { useImmer } from 'use-immer';
import api from '@/api';
import { parseSSEStream } from '@/utils';
import ChatMessages from '@/components/ChatMessages';
import ChatInput from '@/components/ChatInput';
import GraphVisualization from '@/components/GraphVisualization';

function Chatbot() {
  const [chatId, setChatId] = useState(null);
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState('');
  const [graphData, setGraphData] = useState(null);
  const [showGraph, setShowGraph] = useState(false);

  const isLoading = messages.length && messages[messages.length - 1].loading;

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    setMessages(draft => [...draft,
    { role: 'user', content: trimmedMessage },
    { role: 'assistant', content: '', sources: [], loading: true }
    ]);
    setNewMessage('');

    let chatIdOrNew = chatId;
    try {
      if (!chatId) {
        const { id } = await api.createChat();
        setChatId(id);
        chatIdOrNew = id;
      }

      const stream = await api.sendChatMessage(chatIdOrNew, trimmedMessage);
      for await (const textChunk of parseSSEStream(stream)) {
        setMessages(draft => {
          draft[draft.length - 1].content += textChunk;
        });
      }
      setMessages(draft => {
        draft[draft.length - 1].loading = false;
      });

      // Lấy dữ liệu graph visualization
      try {
        const graph = await api.getGraphVisualization(chatIdOrNew, trimmedMessage);
        console.log('Graph data received:', graph);
        setGraphData(graph);
      } catch (err) {
        console.error('Error fetching graph:', err);
      }
    } catch (err) {
      console.log(err);
      setMessages(draft => {
        draft[draft.length - 1].loading = false;
        draft[draft.length - 1].error = true;
      });
    }
  }

  return (
    <div className='relative grow flex flex-col gap-6 pt-6'>
      {messages.length === 0 && (
        <div className='mt-3 font-urbanist text-primary-blue text-xl font-light space-y-2'>
          <p>👋 Chào bạn!</p>
          <p>Tôi là LexiLaw, trợ lý ảo dựa trên trí tuệ nhân tạo chuyên tư vấn các vấn đề liên quan đến Luật Lao động Việt Nam.</p>
          <p>Bạn có câu hỏi hoặc cần giải đáp khúc mắc nào về luật lao động và các vấn đề liên quan không?</p>
        </div>
      )}
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
      />
      {graphData && (
        <div className="flex justify-center">
          <button
            onClick={() => setShowGraph(!showGraph)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            {showGraph ? 'Ẩn đồ thị' : 'Hiển thị đồ thị pháp lý'}
          </button>
        </div>
      )}
      {showGraph && graphData && (
        <GraphVisualization graphData={graphData} />
      )}
      <ChatInput
        newMessage={newMessage}
        isLoading={isLoading}
        setNewMessage={setNewMessage}
        submitNewMessage={submitNewMessage}
      />
    </div>
  );
}

export default Chatbot;