require('dotenv').config({ path: './forge/.env' });

const CHAINGPT_API_KEY = process.env.CHAINGPT_API_KEY;

async function testChainGPT() {
  console.log('Calling ChainGPT API...');
  
  try {
    const response = await fetch('https://api.chaingpt.org/chat/stream', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${CHAINGPT_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'general_assistant',
        question: 'What is Ethereum?',
        chatHistory: 'off'
      })
    });
    
    // Get as text instead of JSON
    const text = await response.text();
    console.log('Response:', text);
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

testChainGPT();