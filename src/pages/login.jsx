import React from 'react';
import Layout from '@theme/Layout';
import Login from '../../services/frontend/src/components/Login';

function LoginPage() {
  return (
    <Layout
      title="Login"
      description="Login to your account"
    >
      <main>
        <Login />
      </main>
    </Layout>
  );
}

export default LoginPage;
