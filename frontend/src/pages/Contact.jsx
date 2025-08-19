import React from 'react'

function Contact() {
    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-6">Contato</h1>
            <div className="max-w-2xl">
                <p className="text-lg text-gray-600 mb-6">
                    Entre em contato conosco para dúvidas sobre o projeto ou suporte técnico.
                </p>

                <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                            <span className="text-primary-600 font-bold">📧</span>
                        </div>
                        <div>
                            <h3 className="font-medium text-gray-900">Email</h3>
                            <p className="text-gray-600">contato@otimizador.com</p>
                        </div>
                    </div>

                    <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                            <span className="text-primary-600 font-bold">💬</span>
                        </div>
                        <div>
                            <h3 className="font-medium text-gray-900">Chat</h3>
                            <p className="text-gray-600">Disponível em horário comercial</p>
                        </div>
                    </div>

                    <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                            <span className="text-primary-600 font-bold">📱</span>
                        </div>
                        <div>
                            <h3 className="font-medium text-gray-900">WhatsApp</h3>
                            <p className="text-gray-600">+55 (11) 99999-9999</p>
                        </div>
                    </div>
                </div>

                <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                    <h3 className="font-medium text-gray-900 mb-2">Horário de Atendimento</h3>
                    <p className="text-gray-600">
                        Segunda a Sexta: 9h às 18h<br />
                        Sábado: 9h às 12h
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Contact
