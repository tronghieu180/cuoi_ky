import React, { useState, useEffect } from "react";
import { FiSearch, FiShoppingCart, FiUser, FiChevronDown, FiMenu, FiX } from "react-icons/fi";
import { FaFacebook, FaInstagram, FaYoutube } from "react-icons/fa";
import { SiZalo } from "react-icons/si";
import SearchProducts from "./SearchProducts";
const Header = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);
    const [cartCount] = useState(0);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 50);
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <header className={`w-full top-0 z-50 sticky border-b border-solid border-gray-500 transition-all duration-300 ${scrolled ? "bg-white shadow-lg" : "bg-transparent"}`}>
            <div className="container mx-auto px-4">
                <div className="flex items-center justify-between h-20">
                    <div className="flex items-center space-x-2 cursor-pointer transform hover:scale-105 transition-transform duration-200">
                        <span className="text-xl font-bold text-gray-800 hidden sm:inline">Tứ Trụ Mobile</span>
                    </div>


                    <nav className="hidden md:flex space-x-8">
                        {["Trang Chủ", "Sản Phẩm", "Khuyến Mãi", "Hỗ Trợ", "Liên Hệ"].map((item) => (
                            <div key={item} className="relative group">
                                <button className="text-gray-700 hover:text-blue-600 font-medium flex items-center">
                                    {item}
                                    {item === "Sản Phẩm" && <FiChevronDown className="ml-1" />}
                                </button>
                                {item === "Sản Phẩm" && (
                                    <div className="absolute hidden group-hover:block w-48 bg-white shadow-lg py-2 rounded-md">
                                        <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50">iPhone</a>
                                        <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50">Samsung</a>
                                        <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50">Xiaomi</a>
                                    </div>
                                )}
                            </div>
                        ))}
                    </nav>

                    <div className="flex items-center space-x-6">
                        <div className="relative">
                            <FiSearch className="h-6 w-6 text-gray-600 hover:text-blue-600 cursor-pointer" />
                        </div>
                        <div className="relative">
                            <FiShoppingCart className="h-6 w-6 text-gray-600 hover:text-blue-600 cursor-pointer" />
                            <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
                                {cartCount}
                            </span>
                        </div>
                        <FiUser className="h-6 w-6 text-gray-600 hover:text-blue-600 cursor-pointer" />
                        <button
                            className="md:hidden"
                            onClick={() => setIsOpen(!isOpen)}
                        >
                            {isOpen ? <FiX className="h-6 w-6" /> : <FiMenu className="h-6 w-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="md:hidden bg-white">
                    <div className="px-2 pt-2 pb-3 space-y-1">
                        {["Trang Chủ", "Sản Phẩm", "Khuyến Mãi", "Hỗ Trợ", "Liên Hệ"].map((item) => (
                            <a
                                key={item}
                                href="#"
                                className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-md"
                            >
                                {item}
                            </a>
                        ))}
                    </div>
                </div>
            )}
        </header>
    );
};

const Footer = () => {
    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    return (
        <footer className="bg-gray-900 text-white pt-12 pb-8">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    <div>
                        <h3 className="text-xl font-bold mb-4">Tứ Trụ Mobile</h3>
                        <p className="text-gray-400 mb-2">68 Võ Văn Tần</p>
                        <p className="text-gray-400 mb-2">Thanh Khê, Đà Nẵng</p>
                        <p className="text-gray-400 mb-2">Phone: (84) 123-456-789</p>
                        <p className="text-gray-400">Email: contact@tutrumobile.com</p>
                    </div>

                    <div>
                        <h3 className="text-xl font-bold mb-4">Giờ làm việc</h3>
                        <p className="text-gray-400 mb-2">Thứ 2 - Thứ 6: 8:00 - 21:00</p>
                        <p className="text-gray-400 mb-2">Thứ 7: 8:00 - 22:00</p>
                        <p className="text-gray-400">Chủ nhật: 9:00 - 21:00</p>
                    </div>

                    <div>
                        <h3 className="text-xl font-bold mb-4">Liên kết nhanh</h3>
                        <ul className="space-y-2">
                            <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Chính Sách</a></li>
                            <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Câu Hỏi Thường Gặp</a></li>
                            <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Điều Khoản Sử Dụng</a></li>
                        </ul>
                    </div>

                    <div className="text-center">
                        <h3 className="text-xl font-bold mb-4">Kết nối với chúng tôi</h3>
                        <div className="flex space-x-4">
                            <FaFacebook className="h-6 w-6 text-gray-400 hover:text-blue-500 cursor-pointer transform hover:scale-110 transition-all" />
                            <FaInstagram className="h-6 w-6 text-gray-400 hover:text-pink-500 cursor-pointer transform hover:scale-110 transition-all" />
                            <SiZalo className="h-6 w-6 text-gray-400 hover:text-blue-400 cursor-pointer transform hover:scale-110 transition-all" />
                            <FaYoutube className="h-6 w-6 text-gray-400 hover:text-red-500 cursor-pointer transform hover:scale-110 transition-all" />
                        </div>
                    </div>
                </div>

                <div className="border-t border-gray-800 mt-8 pt-8 text-center">
                    <p className="text-gray-400">&copy; 2024 Tứ Trụ Mobile. All rights reserved.</p>
                </div>

                <button
                    onClick={scrollToTop}
                    className="fixed bottom-8 right-8 bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full shadow-lg transition-all hover:scale-110"
                    aria-label="Scroll to top"
                >
                    ↑
                </button>
            </div>
        </footer>
    );
};

const Layout = () => {
    return (
        <div className="min-h-screen flex flex-col">
            <Header />
            <main className="flex-grow pt-5">
                <SearchProducts />
            </main>
            <Footer />
        </div>
    );
};

export default Layout;