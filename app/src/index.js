import ReactDOM from 'react-dom';
import App from './App';

window.addEventListener('DOMContentLoaded', (event) => {
  window.formApp = document.getElementById('form-app');
  ReactDOM.render(<App />, window.formApp);
});
