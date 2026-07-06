// Blockchain Transaction Detail Viewer (Shared Library)
async function showTxDetail(txHash) {
    if (!txHash || txHash.trim() === "" || txHash === "None") {
        alert("Mã giao dịch đang được xử lý hoặc chưa được ghi nhận trên chuỗi.");
        return;
    }
    
    let backdrop = document.getElementById('tx-detail-modal-backdrop');
    if (!backdrop) {
        const modalHtml = `
        <div id="tx-detail-modal-backdrop" class="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm hidden items-center justify-center p-4" onclick="handleTxBackdropClick(event)">
          <div id="tx-detail-modal" class="bg-white rounded-[28px] border border-slate-200/80 shadow-2xl max-w-lg w-full overflow-hidden transform scale-95 opacity-0 transition-all duration-300">
            <!-- Modal Header -->
            <div class="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
              <div class="space-y-0.5">
                <span class="text-[9px] uppercase tracking-widest text-slate-400 font-bold text-left block">CHI TIẾT GIAO DỊCH BLOCKCHAIN</span>
                <h3 class="font-bold text-base text-slate-800 flex items-center gap-1.5 font-serif">
                  <i data-lucide="shield" class="w-4.5 h-4.5 text-emerald-600"></i> Bản ghi giao dịch
                </h3>
              </div>
              <button onclick="closeTxDetailModal()" class="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center transition">
                <i data-lucide="x" class="w-4 h-4"></i>
              </button>
            </div>
            
            <!-- Modal Body -->
            <div class="p-6 space-y-4 text-xs text-left" id="tx-detail-modal-body">
              <div class="flex flex-col items-center justify-center py-8 space-y-3">
                <div class="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
                <p class="text-xs text-slate-500 font-medium">Đang kết nối mạng lưới...</p>
              </div>
            </div>
            
            <!-- Modal Footer -->
            <div class="p-4 bg-slate-50/50 border-t border-slate-100 text-center text-[10px] text-slate-400">
              Giao dịch được xác thực an toàn và lưu trữ trên mạng lưới Ethereum.
            </div>
          </div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        backdrop = document.getElementById('tx-detail-modal-backdrop');
    }
    
    const modal = document.getElementById('tx-detail-modal');
    backdrop.classList.remove('hidden');
    backdrop.classList.add('flex');
    setTimeout(() => {
        modal.classList.remove('scale-95', 'opacity-0');
        modal.classList.add('scale-100', 'opacity-100');
    }, 50);
    
    try {
        const response = await fetch(`/products/api/tx/${txHash}/`);
        const data = await response.json();
        
        if (data.success) {
            const bodyEl = document.getElementById('tx-detail-modal-body');
            
            let decoderHtml = '';
            if (data.decoder) {
                decoderHtml = `
                <div class="bg-emerald-50/70 border border-emerald-500/10 rounded-2xl p-4 space-y-3 animate-in-scale">
                  <div class="flex items-start gap-2.5">
                    <div class="w-7 h-7 rounded-full bg-emerald-500/10 text-emerald-700 flex items-center justify-center shrink-0">
                      <i data-lucide="shield" class="w-4 h-4 text-[#007A36]"></i>
                    </div>
                    <div class="space-y-1">
                      <span class="text-[9px] uppercase tracking-widest text-[#007A36] font-bold block">XÁC THỰC TRUY XUẤT NGUỒN GỐC</span>
                      <h4 class="font-bold text-xs text-slate-800">${data.decoder.title}</h4>
                      <p class="text-[11px] text-slate-600 leading-relaxed">${data.decoder.description}</p>
                    </div>
                  </div>
                  <div class="border-t border-emerald-500/10 pt-2.5 grid grid-cols-1 sm:grid-cols-2 gap-2 text-[10px] text-emerald-800 font-medium">
                    <div>Sản phẩm: <span class="text-slate-800 font-semibold">${data.decoder.product_name}</span></div>
                    <div>Nông trại: <span class="text-slate-800 font-semibold">${data.decoder.farm_name}</span></div>
                    <div class="sm:col-span-2">Mã lô hàng: <span class="text-slate-800 font-semibold font-mono">${data.decoder.batch_code}</span></div>
                  </div>
                </div>`;
            } else {
                decoderHtml = `
                <div class="bg-amber-50/50 border border-amber-500/10 rounded-2xl p-4 flex items-start gap-2.5 animate-in-scale">
                  <div class="w-7 h-7 rounded-full bg-amber-500/10 text-amber-700 flex items-center justify-center shrink-0">
                    <i data-lucide="info" class="w-4 h-4 text-amber-600"></i>
                  </div>
                  <div class="space-y-1">
                    <span class="text-[9px] uppercase tracking-widest text-amber-700 font-bold block">Dữ liệu hệ thống</span>
                    <p class="text-[11px] text-amber-900/80 leading-relaxed">Giao dịch hệ thống / Giao dịch quản trị môi trường.</p>
                  </div>
                </div>`;
            }
            
            let warningHtml = '';
            if (data.warning) {
                warningHtml = `
                <div class="bg-amber-50 border border-amber-200/50 rounded-xl p-3 text-[10px] text-amber-800 leading-relaxed mt-3 space-y-1">
                  <div class="font-bold flex items-center gap-1"><i data-lucide="archive" class="w-3.5 h-3.5 text-amber-600"></i> Lưu trữ hệ thống (Archived Data):</div>
                  <p>Dữ liệu lịch sử từ môi trường thử nghiệm trước đó đã được đồng bộ hóa và lưu trữ an toàn trong cơ sở dữ liệu hệ thống.</p>
                </div>`;
            }

            bodyEl.innerHTML = `
              ${decoderHtml}
              ${warningHtml}
              
              <div class="pt-2">
                <!-- Accordion Header -->
                <button onclick="toggleAdvancedTxDetails()" class="w-full flex items-center justify-between py-2.5 text-slate-500 hover:text-slate-700 transition font-bold text-[9px] tracking-wider uppercase border-t border-b border-slate-100 mt-2">
                  <span>Xem chi tiết kỹ thuật</span>
                  <i data-lucide="chevron-down" id="advanced-chevron" class="w-3.5 h-3.5 transition duration-200"></i>
                </button>
                
                <!-- Accordion Content -->
                <div id="advanced-tx-details" class="hidden space-y-4 pt-4 transition-all duration-300">
                  <div class="space-y-1.5">
                    <span class="text-slate-400 block font-semibold">Mã giao dịch (TxHash):</span>
                    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-100 flex items-center justify-between font-mono text-[9.5px] text-slate-800 break-all select-all">
                      <span>${data.tx_hash}</span>
                      <button onclick="copyModalTxHash('${data.tx_hash}', this)" class="w-6 h-6 rounded bg-white hover:bg-slate-100 border border-slate-200 flex items-center justify-center shrink-0 ml-2" title="Sao chép">
                        <i data-lucide="copy" class="w-3.5 h-3.5 text-slate-500"></i>
                      </button>
                    </div>
                  </div>
                  
                  <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-1">
                      <span class="text-slate-400 block font-semibold">Trạng thái:</span>
                      <div class="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded-full font-bold">${data.status}</div>
                    </div>
                    <div class="space-y-1">
                      <span class="text-slate-400 block font-semibold">Mã khối (Block):</span>
                      <div class="font-bold text-slate-800">#${data.block_number}</div>
                    </div>
                  </div>
                  
                  <div class="space-y-1">
                    <span class="text-slate-400 block font-semibold">Thời gian đào khối (Block Time):</span>
                    <div class="font-semibold text-slate-800">${data.timestamp}</div>
                  </div>
                  
                  <div class="space-y-2 pt-2 border-t border-slate-100">
                    <div class="space-y-1">
                      <span class="text-slate-400 block font-semibold">Địa chỉ gửi (From / Actor):</span>
                      <div class="font-mono bg-slate-50 p-2 rounded-xl border border-slate-100 text-[9.5px] break-all select-all">${data.from_addr}</div>
                    </div>
                    <div class="space-y-1">
                      <span class="text-slate-400 block font-semibold">Địa chỉ nhận (To / Contract):</span>
                      <div class="font-mono bg-slate-50 p-2 rounded-xl border border-slate-100 text-[9.5px] break-all select-all">${data.to_addr}</div>
                    </div>
                  </div>
                  
                  <div class="flex justify-between items-center border-t border-slate-100 pt-3 text-[11px]">
                    <span class="text-slate-400 font-semibold">Năng lượng tiêu hao (Gas Used):</span>
                    <strong class="font-mono text-slate-800">${data.gas_used.toLocaleString()}</strong>
                  </div>
                </div>
              </div>
            `;
            if (window.lucide) {
                window.lucide.createIcons();
            }
        } else {
            showErrorInModal(data.error || "Không thể tải chi tiết giao dịch.");
        }
    } catch (error) {
        showErrorInModal("Lỗi kết nối máy chủ Blockchain.");
    }
}

function toggleAdvancedTxDetails() {
    const content = document.getElementById('advanced-tx-details');
    const chevron = document.getElementById('advanced-chevron');
    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        chevron.classList.add('rotate-180');
    } else {
        content.classList.add('hidden');
        chevron.classList.remove('rotate-180');
    }
}

function showErrorInModal(msg) {
    const bodyEl = document.getElementById('tx-detail-modal-body');
    bodyEl.innerHTML = `
      <div class="text-center py-6 space-y-2.5">
        <div class="w-10 h-10 rounded-full bg-rose-50 flex items-center justify-center text-rose-500 mx-auto">
          <i data-lucide="alert-circle" class="w-5 h-5"></i>
        </div>
        <p class="text-xs font-semibold text-slate-800">Truy vấn giao dịch thất bại</p>
        <p class="text-[11px] text-slate-500 max-w-xs mx-auto leading-relaxed">${msg}</p>
      </div>
    `;
    if (window.lucide) {
        window.lucide.createIcons();
    }
}

function closeTxDetailModal() {
    const backdrop = document.getElementById('tx-detail-modal-backdrop');
    const modal = document.getElementById('tx-detail-modal');
    if (modal && backdrop && !backdrop.classList.contains('hidden')) {
        modal.classList.remove('scale-100', 'opacity-100');
        modal.classList.add('scale-95', 'opacity-0');
        setTimeout(() => {
            backdrop.classList.add('hidden');
            backdrop.classList.remove('flex');
        }, 300);
    }
}

function handleTxBackdropClick(event) {
    if (event.target === document.getElementById('tx-detail-modal-backdrop')) {
        closeTxDetailModal();
    }
}

function copyModalTxHash(hash, btn) {
    navigator.clipboard.writeText(hash).then(() => {
        const originalContent = btn.innerHTML;
        btn.innerHTML = `<i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600"></i>`;
        if (window.lucide) window.lucide.createIcons();
        setTimeout(() => {
            btn.innerHTML = originalContent;
            if (window.lucide) window.lucide.createIcons();
        }, 2000);
    });
}
