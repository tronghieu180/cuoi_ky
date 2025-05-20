import React, { useState, useEffect } from "react";
import { FiSearch, FiChevronLeft, FiChevronRight } from "react-icons/fi";
import { BsFilterLeft, BsSortUp, BsSortDown } from "react-icons/bs";

const DB_API_URL = "http://localhost:8080/db";
const ITEMS_PER_PAGE = 6;

export default function SearchProducts() {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [filters, setFilters] = useState({ type: "", category: "", minPrice: "", maxPrice: "" });
  const [sortConfig, setSortConfig] = useState({ field: "", direction: "" });
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  const totalPages = Math.ceil(filteredProducts.length / ITEMS_PER_PAGE);
  const paginatedProducts = filteredProducts.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  const handleSort = (field) => {
    const direction =
      sortConfig.field === field && sortConfig.direction === "asc" ? "desc" : "asc";
    setSortConfig({ field, direction });
  };

  const clearFilters = () => {
    setFilters({ type: "", category: "", minPrice: "", maxPrice: "" });
    setSortConfig({ field: "", direction: "" });
    setFilteredProducts(results); // Reset filteredProducts về results gốc
    setCurrentPage(1);
  };

  const search = async () => {
    const actualKeyword = keyword.trim() === "" ? "a" : keyword.trim();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${DB_API_URL}/search?keyword=${encodeURIComponent(actualKeyword)}`);
      if (!res.ok) throw new Error(`Error: ${res.status}`);
      const data = await res.json();
      setResults(data);
      setFilteredProducts(data); // Hiển thị toàn bộ kết quả tìm kiếm ban đầu
    } catch (err) {
      setError(err.message || "Lỗi khi tìm kiếm");
      setResults([]);
      setFilteredProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...results];
    if (filters.type) filtered = filtered.filter((p) => p.type === filters.type);
    if (filters.category) filtered = filtered.filter((p) => p.category === filters.category);
    if (filters.minPrice) filtered = filtered.filter((p) => Number(p.price) >= Number(filters.minPrice));
    if (filters.maxPrice) filtered = filtered.filter((p) => Number(p.price) <= Number(filters.maxPrice));

    if (sortConfig.field && sortConfig.direction) {
      filtered.sort((a, b) => {
        const diff = Number(a[sortConfig.field]) - Number(b[sortConfig.field]);
        return sortConfig.direction === "asc" ? diff : -diff;
      });
    }

    setFilteredProducts(filtered);
    setCurrentPage(1);
  };

  // Chỉ gọi applyFilters khi filters hoặc sortConfig thay đổi
  useEffect(() => {
    if (filters.type || filters.category || filters.minPrice || filters.maxPrice || sortConfig.field) {
      applyFilters();
    }
  }, [filters, sortConfig]);

  // Tìm kiếm lần đầu khi component được mount
  useEffect(() => {
    search();
  }, []);

  const onSubmit = (e) => {
    e.preventDefault();
    search();
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <form onSubmit={onSubmit} className="mb-4 flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="Nhập từ khóa tìm kiếm..."
            className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
          Tìm kiếm
        </button>
      </form>

      <button
        className="md:hidden flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg mb-4"
        onClick={() => setIsFilterOpen(!isFilterOpen)}
      >
        <BsFilterLeft /> Bộ lọc
      </button>

      <div className={`${isFilterOpen ? "block" : "hidden md:block"}`}>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <select
            className="p-2 border rounded-lg"
            value={filters.type}
            onChange={(e) => setFilters({ ...filters, type: e.target.value })}
          >
            <option value="">Tất cả loại</option>
            <option value="Electronics">Electronics</option>
            <option value="Furniture">Furniture</option>
          </select>

          <select
            className="p-2 border rounded-lg"
            value={filters.category}
            onChange={(e) => setFilters({ ...filters, category: e.target.value })}
          >
            <option value="">Tất cả danh mục</option>
            <option value="Audio">Audio</option>
            <option value="Office">Office</option>
            <option value="Wearables">Wearables</option>
          </select>

          <input
            type="number"
            placeholder="Giá tối thiểu"
            className="p-2 border rounded-lg"
            value={filters.minPrice}
            onChange={(e) => setFilters({ ...filters, minPrice: e.target.value })}
          />

          <input
            type="number"
            placeholder="Giá tối đa"
            className="p-2 border rounded-lg"
            value={filters.maxPrice}
            onChange={(e) => setFilters({ ...filters, maxPrice: e.target.value })}
          />
        </div>

        <div className="flex gap-4 mb-6">
          <button
            className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            onClick={() => handleSort("price")}
          >
            {sortConfig.field === "price" && sortConfig.direction === "asc" ? (
              <BsSortUp />
            ) : (
              <BsSortDown />
            )}
            Sắp xếp theo giá
          </button>

          <button
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            onClick={applyFilters}
          >
            Áp dụng bộ lọc
          </button>

          <button
            className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300"
            onClick={clearFilters}
          >
            Xóa bộ lọc
          </button>
        </div>
      </div>

      {loading && <p className="text-blue-500">Đang tìm kiếm...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {paginatedProducts.length === 0 && !loading ? (
        <div className="text-center py-8 text-gray-500">
          Không có sản phẩm phù hợp
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {paginatedProducts.map((item) => (
            <div
              key={item.id}
              className="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow"
            >
              <img
                src={item.image_link}
                alt={item.title}
                className="w-full h-auto object-contain"
                loading="lazy"
              />
              <div className="p-4">
                <h3 className="text-lg font-semibold mb-2">{item.title}</h3>
                <div className="flex justify-between text-sm text-gray-600">
                  <span>{item.type === "phone" ? "Điện thoại" :
                    item.type === "tablet" ? "Máy tính bảng" :
                      item.type === "accessory" ? "Phụ kiện" :
                        item.type
                  }</span>
                  <span>{item.category}</span>
                </div>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-green-600 font-bold">{Number(item.price).toLocaleString("vi-VN")} VNĐ</span>
                  <a
                    href={item.link}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-500 underline"
                  >
                    Chi tiết
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div className="mt-8 flex items-center justify-between">
          <span className="text-sm text-gray-600">
            Hiển thị {(currentPage - 1) * ITEMS_PER_PAGE + 1} đến{" "}
            {Math.min(currentPage * ITEMS_PER_PAGE, filteredProducts.length)} trong{" "}
            {filteredProducts.length} sản phẩm
          </span>

          <div className="flex items-center gap-2">
            <button
              className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={currentPage === 1}
            >
              <FiChevronLeft />
            </button>

            {[...Array(totalPages)].map((_, i) => i + 1)
              .filter((page) => {
                return (
                  page === 1 ||
                  page === totalPages ||
                  Math.abs(page - currentPage) <= 1
                );
              })
              .reduce((acc, page, index, arr) => {
                if (index > 0 && page - arr[index - 1] > 1) {
                  acc.push("ellipsis");
                }
                acc.push(page);
                return acc;
              }, [])
              .map((item, idx) =>
                item === "ellipsis" ? (
                  <span key={`ellipsis-${idx}`} className="px-2 text-gray-500">
                    ...
                  </span>
                ) : (
                  <button
                    key={item}
                    className={`rounded-lg text-center   ${currentPage === item
                      ? "bg-blue-500 text-white"
                      : "bg-gray-100 hover:bg-gray-200"
                      }`}
                    onClick={() => setCurrentPage(item)}
                  >
                    {item}
                  </button>
                )
              )}

            <button
              className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              <FiChevronRight />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}