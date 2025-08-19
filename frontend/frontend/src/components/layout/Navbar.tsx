import React from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
    return (
        <nav className="bg-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex justify-between h-16">
                    <div className="flex items-center">
                        <Link to="/" className="text-xl font-bold text-gray-800">
                            Otimizador de CV
                        </Link>
                    </div>

                    <div className="flex items-center space-x-4">
                        <Link
                            to="/dashboard"
                            className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Dashboard
                        </Link>
                        <Link
                            to="/profile"
                            className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Perfil
                        </Link>
                        <button
                            className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
                            onClick={() => {
                                localStorage.removeItem('authToken');
                                window.location.href = '/login';
                            }}
                        >
                            Sair
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
