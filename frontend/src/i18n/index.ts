import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Importar las traducciones
import es from './locales/es.json';
import en from './locales/en.json';
import pt from './locales/pt.json';

const resources = {
  es: {
    translation: es
  },
  en: {
    translation: en
  },
  pt: {
    translation: pt
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: localStorage.getItem('language') || 'es', // Idioma por defecto
    fallbackLng: 'es',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
