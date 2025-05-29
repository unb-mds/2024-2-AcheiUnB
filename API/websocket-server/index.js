require('dotenv').config();
const express = require('express');
const http = require('http');
const cors = require('cors');
const { Server } = require('socket.io');
const axios = require('axios');

const app = express();
app.use(cors());

const server = http.createServer(app);

const io = new Server(server, {
    cors: {
        origin: process.env.FRONTEND_URL || "http://localhost:3000",
        methods: ["GET", "POST"],   
    },
});

io.on('connection', (socket) => {
    console.log(`User connected: ${socket.id}`);

    // Entrar na sala do chat
    socket.on('join_room', (data) => {
        if (data?.chatroom_id) {
            socket.join(data.chatroom_id.toString());
            console.log(`Socket ${socket.id} entrou na sala ${data.chatroom_id}`);
        }
    });

    socket.on('send_message', (data) => {
        console.log('Recebido send_message:', data);
        // Garante que a mensagem seja emitida apenas para a sala correta
        io.to(data.room.toString()).emit('receive_message', data);
    });

    socket.on('read_message', async (data) => {
        console.log('Recebido read_message:', data);
        // Atualiza o Django para cada mensagem lida
        if (Array.isArray(data.message_ids)) {
            for (const messageId of data.message_ids) {
                try {
                    const resp = await axios.post(
                        `https://localhost:8080/api/chat/messages/${messageId}/mark_as_read/`,
                        {},
                        {
                            // Se precisar autenticação, adicione aqui
                            // headers: { Authorization: `Bearer <TOKEN>` }
                        }
                    );
                    console.log(`Mensagem ${messageId} marcada como lida no Django. Status:`, resp.status);
                } catch (err) {
                    console.error('Erro ao marcar mensagem como lida no Django:', err.message);
                }
            }
        }
        // Notifica a sala
        console.log('Emitindo message_read para sala', data.chatroom_id, 'com dados:', data);
        io.to(data.chatroom_id.toString()).emit('message_read', data);
    });

    socket.on('disconnect', () => {
        console.log(`User disconnected: ${socket.id}`);
    });
});
const PORT = process.env.WEBSOCKET_PORT || 4000;
server.listen(PORT, () => {
    console.log(`WebSocket server is running on port ${PORT}`);
});