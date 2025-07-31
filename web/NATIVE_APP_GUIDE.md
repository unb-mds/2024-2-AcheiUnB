# AcheiUnB App Nativo - Cordova

Este é um guia para criar um aplicativo nativo do AcheiUnB usando Apache Cordova.

## 🚀 Instalação do Cordova

### Pré-requisitos
- Node.js 18+
- Java JDK 11 ou superior
- Android Studio (para Android)
- Xcode (para iOS - apenas macOS)

### Instalação global do Cordova
```bash
npm install -g cordova
```

### Configuração do projeto
```bash
# Criar projeto Cordova
cordova create acheiunb-app com.acheiunb.app AcheiUnB
cd acheiunb-app

# Adicionar plataformas
cordova platform add android
cordova platform add ios  # apenas no macOS
```

## 📱 Configuração do config.xml

```xml
<?xml version='1.0' encoding='utf-8'?>
<widget id="com.acheiunb.app" version="1.0.0" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    <name>AcheiUnB</name>
    <description>
        Aplicativo para encontrar e vender itens na UnB
    </description>
    <author email="contato@acheiunb.com.br" href="https://acheiunb.com.br">
        Equipe AcheiUnB
    </author>
    <content src="index.html" />
    <access origin="*" />
    <allow-intent href="http://*/*" />
    <allow-intent href="https://*/*" />
    <allow-intent href="tel:*" />
    <allow-intent href="sms:*" />
    <allow-intent href="mailto:*" />
    <allow-intent href="geo:*" />
    
    <platform name="android">
        <allow-intent href="market:*" />
        <icon density="ldpi" src="res/icon/android/ldpi.png" />
        <icon density="mdpi" src="res/icon/android/mdpi.png" />
        <icon density="hdpi" src="res/icon/android/hdpi.png" />
        <icon density="xhdpi" src="res/icon/android/xhdpi.png" />
        <icon density="xxhdpi" src="res/icon/android/xxhdpi.png" />
        <icon density="xxxhdpi" src="res/icon/android/xxxhdpi.png" />
        
        <splash density="land-ldpi" src="res/screen/android/land-ldpi.png" />
        <splash density="land-mdpi" src="res/screen/android/land-mdpi.png" />
        <splash density="land-hdpi" src="res/screen/android/land-hdpi.png" />
        <splash density="land-xhdpi" src="res/screen/android/land-xhdpi.png" />
        <splash density="land-xxhdpi" src="res/screen/android/land-xxhdpi.png" />
        <splash density="land-xxxhdpi" src="res/screen/android/land-xxxhdpi.png" />
        
        <preference name="SplashScreenDelay" value="3000" />
        <preference name="SplashMaintainAspectRatio" value="true" />
        <preference name="SplashShowOnlyFirstTime" value="false" />
    </platform>
    
    <platform name="ios">
        <allow-intent href="itms:*" />
        <allow-intent href="itms-apps:*" />
        <icon height="180" src="res/icon/ios/icon-60-3x.png" width="180" />
        <icon height="60" src="res/icon/ios/icon-60.png" width="60" />
        <icon height="120" src="res/icon/ios/icon-60-2x.png" width="120" />
        <icon height="76" src="res/icon/ios/icon-76.png" width="76" />
        <icon height="152" src="res/icon/ios/icon-76-2x.png" width="152" />
        <icon height="40" src="res/icon/ios/icon-40.png" width="40" />
        <icon height="80" src="res/icon/ios/icon-40-2x.png" width="80" />
        <icon height="57" src="res/icon/ios/icon-57.png" width="57" />
        <icon height="114" src="res/icon/ios/icon-57-2x.png" width="114" />
        <icon height="72" src="res/icon/ios/icon-72.png" width="72" />
        <icon height="144" src="res/icon/ios/icon-72-2x.png" width="144" />
        <icon height="29" src="res/icon/ios/icon-small.png" width="29" />
        <icon height="58" src="res/icon/ios/icon-small-2x.png" width="58" />
        <icon height="50" src="res/icon/ios/icon-50.png" width="50" />
        <icon height="100" src="res/icon/ios/icon-50-2x.png" width="100" />
        
        <preference name="SplashScreenDelay" value="3000" />
        <preference name="FadeSplashScreenDuration" value="300" />
        <preference name="SplashShowOnlyFirstTime" value="false" />
    </platform>
    
    <!-- Plugins -->
    <plugin name="cordova-plugin-whitelist" spec="^1.3.4" />
    <plugin name="cordova-plugin-statusbar" spec="^2.4.2" />
    <plugin name="cordova-plugin-device" spec="^2.0.3" />
    <plugin name="cordova-plugin-splashscreen" spec="^5.0.3" />
    <plugin name="cordova-plugin-inappbrowser" spec="^4.0.0" />
    <plugin name="cordova-plugin-network-information" spec="^2.0.2" />
    
    <!-- Preferências -->
    <preference name="StatusBarOverlaysWebView" value="false" />
    <preference name="StatusBarBackgroundColor" value="#E97316" />
    <preference name="StatusBarStyle" value="lightcontent" />
    <preference name="Fullscreen" value="false" />
    <preference name="Orientation" value="portrait" />
    <preference name="DisallowOverscroll" value="true" />
    <preference name="BackgroundColor" value="0xFFE97316" />
    <preference name="HideKeyboardFormAccessoryBar" value="true" />
    <preference name="KeyboardDisplayRequiresUserAction" value="false" />
</widget>
```

## 📝 Arquivo index.html principal

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>AcheiUnB</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #E97316;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: white;
        }
        
        .loading {
            text-align: center;
        }
        
        .logo {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            font-weight: bold;
            color: #E97316;
            margin-left: auto;
            margin-right: auto;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .hidden {
            display: none;
        }
        
        #webview {
            width: 100%;
            height: 100vh;
            border: none;
        }
        
        .error {
            background: #ff4444;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div id="loading" class="loading">
        <div class="logo">AU</div>
        <h1>AcheiUnB</h1>
        <div class="spinner"></div>
        <p>Carregando...</p>
    </div>
    
    <div id="error" class="error hidden">
        <h3>Erro de Conexão</h3>
        <p>Não foi possível conectar ao AcheiUnB. Verifique sua conexão com a internet.</p>
        <button onclick="reloadApp()">Tentar Novamente</button>
    </div>
    
    <iframe id="webview" class="hidden" src=""></iframe>
    
    <script type="text/javascript" src="cordova.js"></script>
    <script type="text/javascript">
        const WEBSITE_URL = 'https://acheiunb.com.br';
        
        document.addEventListener('deviceready', function() {
            console.log('Device is ready');
            
            // Verificar conexão
            if (navigator.connection.type === Connection.NONE) {
                showError();
                return;
            }
            
            // Configurar status bar
            if (window.StatusBar) {
                StatusBar.overlaysWebView(false);
                StatusBar.backgroundColorByHexString('#E97316');
                StatusBar.styleLightContent();
            }
            
            // Carregar website
            loadWebsite();
            
            // Escutar mudanças na conexão
            document.addEventListener('online', function() {
                console.log('Online');
                if (document.getElementById('webview').src === '') {
                    loadWebsite();
                }
            });
            
            document.addEventListener('offline', function() {
                console.log('Offline');
                showError();
            });
            
        }, false);
        
        function loadWebsite() {
            const webview = document.getElementById('webview');
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            
            // Esconder erro se estiver visível
            error.classList.add('hidden');
            
            // Mostrar loading
            loading.classList.remove('hidden');
            webview.classList.add('hidden');
            
            // Carregar o site
            webview.src = WEBSITE_URL;
            
            // Quando carregar, esconder loading
            webview.onload = function() {
                setTimeout(() => {
                    loading.classList.add('hidden');
                    webview.classList.remove('hidden');
                }, 1000);
            };
            
            // Se der erro, mostrar tela de erro
            webview.onerror = function() {
                showError();
            };
        }
        
        function showError() {
            document.getElementById('loading').classList.add('hidden');
            document.getElementById('webview').classList.add('hidden');
            document.getElementById('error').classList.remove('hidden');
        }
        
        function reloadApp() {
            location.reload();
        }
        
        // Interceptar links externos
        document.addEventListener('click', function(e) {
            if (e.target.tagName === 'A' && e.target.href.startsWith('http')) {
                e.preventDefault();
                window.open(e.target.href, '_system');
            }
        });
    </script>
</body>
</html>
```

## 🔧 Comandos de Build

### Android
```bash
# Instalar plugins
cordova plugin add cordova-plugin-whitelist
cordova plugin add cordova-plugin-statusbar
cordova plugin add cordova-plugin-device
cordova plugin add cordova-plugin-splashscreen
cordova plugin add cordova-plugin-inappbrowser
cordova plugin add cordova-plugin-network-information

# Build para Android
cordova build android

# Build para release
cordova build android --release

# Executar no emulador
cordova emulate android

# Executar no device
cordova run android
```

### iOS
```bash
# Build para iOS
cordova build ios

# Abrir no Xcode
open platforms/ios/AcheiUnB.xcworkspace
```

## 📱 Geração de Ícones

Use o serviço [App Icon Generator](https://www.appicon.co/) para gerar todos os tamanhos de ícone necessários a partir do seu logo.

## 📦 Distribuição

### Android (Google Play Store)
1. Gere um APK assinado
2. Crie uma conta no Google Play Console
3. Suba o APK e configure a listagem
4. Publique o app

### iOS (App Store)
1. Configure provisioning profiles no Xcode
2. Crie uma conta no Apple Developer Program
3. Use o Xcode para fazer upload para o App Store Connect
4. Configure a listagem e publique

## 🔄 Atualizações

Como o app carrega o website, as atualizações são automáticas. Você só precisa atualizar o app nativo quando:
- Mudar ícones ou splash screens
- Adicionar novos plugins
- Alterar configurações nativas

## 🎯 Vantagens do App Nativo

- **Distribuição nas App Stores**: Maior visibilidade
- **Ícone na tela inicial**: Fácil acesso
- **Notificações Push**: Comunicação direta com usuários
- **Funcionalidades nativas**: Câmera, GPS, etc.
- **Offline primeira**: Melhor experiência sem internet

## 📋 Próximos Passos

1. [ ] Configurar notificações push
2. [ ] Adicionar funcionalidades nativas (câmera, GPS)
3. [ ] Implementar cache inteligente
4. [ ] Configurar deep links
5. [ ] Testes em dispositivos reais
6. [ ] Publicação nas app stores
