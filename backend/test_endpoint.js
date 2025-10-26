const axios = require('axios');

async function testEndpoint() {
  try {
    console.log('Testing /api/test-advisor/recommend endpoint...');
    
    const response = await axios.post('http://localhost:3001/api/test-advisor/recommend', {
      researchQuestion: 'compare_groups',
      nGroups: 2,
      outcomeType: 'continuous',
      isNormal: true,
      isPaired: false
    });
    
    console.log('✅ Success!');
    console.log('Response:', JSON.stringify(response.data, null, 2));
    
    if (response.data.ok && response.data.recommendations) {
      console.log(`\n✅ Got ${response.data.recommendations.length} recommendations`);
      console.log(`First test: ${response.data.recommendations[0].test_name}`);
    }
  } catch (error) {
    console.error('❌ Error:', error.response?.data || error.message);
    console.error('Status:', error.response?.status);
  }
}

testEndpoint();
