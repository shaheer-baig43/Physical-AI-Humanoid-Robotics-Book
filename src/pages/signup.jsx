import React from 'react';
import Layout from '@theme/Layout';
import Signup from '../../services/frontend/src/components/Signup';

function SignupPage() {
  return (
    <Layout
      title="Signup"
      description="Create an account and complete your profile"
    >
      <main>
        <Signup />
      </main>
    </Layout>
  );
}

export default SignupPage;
