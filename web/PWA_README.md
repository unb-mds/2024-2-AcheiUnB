# AcheiUnB PWA - Aplicativo Mobile

O AcheiUnB agora pode ser instalado como um aplicativo no seu dispositivo móvel!

## 🚀 Como instalar o app

### Android (Chrome/Edge/Samsung Internet)
1. Acesse https://acheiunb.com.br no seu navegador
2. Toque no ícone de "Adicionar à tela inicial" ou "Instalar app"
3. Confirme a instalação
4. O app aparecerá na sua tela inicial

### iOS (Safari)
1. Acesse https://acheiunb.com.br no Safari
2. Toque no ícone de compartilhar (quadrado com seta)
3. Selecione "Adicionar à Tela de Início"
4. Toque em "Adicionar"

### Desktop (Chrome/Edge/Firefox)
1. Acesse https://acheiunb.com.br
2. Clique no ícone de instalação na barra de endereços
3. Ou acesse Menu > Instalar AcheiUnB
4. Confirme a instalação

## ✨ Funcionalidades do PWA

- **Funciona offline**: Visualize itens salvos mesmo sem internet
- **Instalação nativa**: Comporta-se como um app real
- **Atualizações automáticas**: Sempre atualizado para a versão mais recente
- **Notificações**: Receba alertas sobre novos itens (futuro)
- **Compartilhamento**: Compartilhe itens diretamente do app

## 🔧 Configuração para Desenvolvedores

### Pré-requisitos
- Node.js 18+
- npm ou yarn

### Instalação
```bash
cd web
npm install
```

### Desenvolvimento
```bash
npm run dev
```

### Build de Produção
```bash
npm run build
```

### Testando PWA localmente
```bash
npm run build
npm run preview
```

## 📱 Configurações PWA

O app está configurado com:
- **Tema**: Laranja (#E97316)
- **Display**: Standalone (tela cheia)
- **Orientação**: Portrait
- **Cache**: Estratégia Network-First para API calls
- **Ícones**: Múltiplos tamanhos para diferentes dispositivos

## 🛠️ Estrutura de Arquivos

```
web/
├── public/
│   ├── offline.html          # Página offline
│   └── manifest.json         # Manifesto PWA (gerado automaticamente)
├── src/
│   ├── components/
│   │   ├── InstallPrompt.vue # Prompt de instalação
│   │   └── SplashScreen.vue  # Tela de carregamento
│   └── main.js               # Registro do Service Worker
├── vite.config.js            # Configuração PWA
└── package.json
```

## 🚀 Deploy

O PWA é buildado automaticamente para a pasta `../API/AcheiUnB/static/dist/` e servido pelo Django.

## 📋 Checklist PWA

- [x] Manifesto configurado
- [x] Service Worker registrado
- [x] Ícones em múltiplos tamanhos
- [x] Página offline
- [x] Meta tags mobile
- [x] Tema configurado
- [x] Prompt de instalação
- [x] Cache de API
- [x] Atualização automática

## 🔄 Atualizações

O PWA se atualiza automaticamente quando uma nova versão é implantada. Os usuários verão suas alterações na próxima vez que abrirem o app.

## 🐛 Problemas Conhecidos

- [ ] Notificações push (em desenvolvimento)
- [ ] Sincronização em background (futuro)
- [ ] Compartilhamento nativo (futuro)

## 📞 Suporte

Para problemas relacionados ao PWA, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.
