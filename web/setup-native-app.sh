#!/bin/bash

# Script para configurar o app nativo do AcheiUnB
# Uso: ./setup-native-app.sh

echo "🚀 Configurando AcheiUnB App Nativo com Cordova"
echo "=============================================="

# Verificar se o Cordova está instalado
if ! command -v cordova &> /dev/null; then
    echo "❌ Cordova não encontrado. Instalando..."
    npm install -g cordova
fi

# Criar diretório para o app
APP_DIR="../acheiunb-app"
echo "📁 Criando projeto em $APP_DIR"

# Remover diretório se existir
if [ -d "$APP_DIR" ]; then
    echo "🗑️  Removendo projeto existente..."
    rm -rf "$APP_DIR"
fi

# Criar novo projeto Cordova
cordova create "$APP_DIR" com.acheiunb.app AcheiUnB
cd "$APP_DIR"

# Adicionar plataformas
echo "📱 Adicionando plataformas..."
cordova platform add android

# Verificar se estamos no macOS para adicionar iOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Detectado macOS. Adicionando plataforma iOS..."
    cordova platform add ios
fi

# Instalar plugins essenciais
echo "🔌 Instalando plugins..."
cordova plugin add cordova-plugin-whitelist
cordova plugin add cordova-plugin-statusbar
cordova plugin add cordova-plugin-device
cordova plugin add cordova-plugin-splashscreen
cordova plugin add cordova-plugin-inappbrowser
cordova plugin add cordova-plugin-network-information

# Copiar arquivos de configuração
echo "⚙️  Copiando arquivos de configuração..."

# Criar config.xml
cat > config.xml << 'EOF'
<?xml version='1.0' encoding='utf-8'?>
<widget id="com.acheiunb.app" version="1.0.0" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    <name>AcheiUnB</name>
    <description>Aplicativo para encontrar e vender itens na UnB</description>
    <author email="contato@acheiunb.com.br" href="https://acheiunb.com.br">Equipe AcheiUnB</author>
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
        <preference name="SplashScreenDelay" value="3000" />
        <preference name="SplashMaintainAspectRatio" value="true" />
        <preference name="SplashShowOnlyFirstTime" value="false" />
    </platform>
    
    <platform name="ios">
        <allow-intent href="itms:*" />
        <allow-intent href="itms-apps:*" />
        <preference name="SplashScreenDelay" value="3000" />
        <preference name="FadeSplashScreenDuration" value="300" />
        <preference name="SplashShowOnlyFirstTime" value="false" />
    </platform>
    
    <plugin name="cordova-plugin-whitelist" spec="^1.3.4" />
    <plugin name="cordova-plugin-statusbar" spec="^2.4.2" />
    <plugin name="cordova-plugin-device" spec="^2.0.3" />
    <plugin name="cordova-plugin-splashscreen" spec="^5.0.3" />
    <plugin name="cordova-plugin-inappbrowser" spec="^4.0.0" />
    <plugin name="cordova-plugin-network-information" spec="^2.0.2" />
    
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
EOF

# Criar index.html customizado
cat > www/index.html << 'EOF'
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
            
            if (navigator.connection && navigator.connection.type === Connection.NONE) {
                showError();
                return;
            }
            
            if (window.StatusBar) {
                StatusBar.overlaysWebView(false);
                StatusBar.backgroundColorByHexString('#E97316');
                StatusBar.styleLightContent();
            }
            
            loadWebsite();
            
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
            
            error.classList.add('hidden');
            loading.classList.remove('hidden');
            webview.classList.add('hidden');
            
            webview.src = WEBSITE_URL;
            
            webview.onload = function() {
                setTimeout(() => {
                    loading.classList.add('hidden');
                    webview.classList.remove('hidden');
                }, 1000);
            };
            
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
        
        document.addEventListener('click', function(e) {
            if (e.target.tagName === 'A' && e.target.href.startsWith('http')) {
                e.preventDefault();
                window.open(e.target.href, '_system');
            }
        });
    </script>
</body>
</html>
EOF

# Criar script de build
cat > build.sh << 'EOF'
#!/bin/bash

echo "🔨 Fazendo build do AcheiUnB App..."

# Build para Android
echo "📱 Building Android..."
cordova build android

# Build para iOS (se disponível)
if cordova platform ls | grep -q "ios"; then
    echo "🍎 Building iOS..."
    cordova build ios
fi

echo "✅ Build concluído!"
echo "📦 Arquivos gerados:"
echo "   Android: platforms/android/app/build/outputs/apk/debug/app-debug.apk"
if cordova platform ls | grep -q "ios"; then
    echo "   iOS: platforms/ios/AcheiUnB.xcworkspace"
fi
EOF

chmod +x build.sh

# Criar script de run
cat > run.sh << 'EOF'
#!/bin/bash

echo "🚀 Executando AcheiUnB App..."

# Verificar se há dispositivos Android conectados
if adb devices | grep -q "device"; then
    echo "📱 Executando no dispositivo Android..."
    cordova run android
else
    echo "📱 Executando no emulador Android..."
    cordova emulate android
fi
EOF

chmod +x run.sh

echo ""
echo "✅ Configuração concluída!"
echo "📍 Projeto criado em: $APP_DIR"
echo ""
echo "🎯 Próximos passos:"
echo "1. cd $APP_DIR"
echo "2. ./build.sh    # Para fazer build"
echo "3. ./run.sh      # Para executar no dispositivo/emulador"
echo ""
echo "📱 Para Android:"
echo "   - Instale o Android Studio"
echo "   - Configure o SDK Android"
echo "   - Conecte um dispositivo ou inicie um emulador"
echo ""
echo "🍎 Para iOS (apenas macOS):"
echo "   - Instale o Xcode"
echo "   - Configure uma conta de desenvolvedor Apple"
echo "   - Abra o arquivo .xcworkspace no Xcode"
echo ""
echo "📚 Documentação completa em: NATIVE_APP_GUIDE.md"
