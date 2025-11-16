// Admin dashboard JavaScript
let adminToken = '';

function getAuthHeaders() {
    return {
        'Content-Type': 'application/json',
        'X-Admin-Token': adminToken || document.getElementById('adminToken').value
    };
}

async function loadClaims() {
    try {
        const response = await fetch('/admin/claims?token=' + (adminToken || document.getElementById('adminToken').value));
        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        const list = document.getElementById('claimsList');
        list.innerHTML = '';
        
        data.claims.forEach(claim => {
            const item = document.createElement('div');
            item.className = 'claim-item';
            item.innerHTML = `
                <div class="claim-header">
                    <div>
                        <strong>Claim #${claim.id}</strong>
                        <span style="margin-left: 12px; padding: 4px 8px; background: ${claim.status === 'pending' ? '#ff9800' : claim.status === 'approved' ? '#4caf50' : '#f44336'}; color: #fff; border-radius: 4px; font-size: 12px;">${claim.status}</span>
                    </div>
                    <div class="claim-actions">
                        ${claim.status === 'pending' ? `
                            <button class="btn-action btn-approve" onclick="approveClaim(${claim.id})">Approve</button>
                            <button class="btn-action btn-reject" onclick="rejectClaim(${claim.id})">Reject</button>
                            ${claim.prize.type === 'ton' ? `<button class="btn-action btn-payout" onclick="processPayout(${claim.id})">Payout</button>` : ''}
                        ` : ''}
                    </div>
                </div>
                <div style="margin-top: 8px;">
                    <div>User: ${claim.user.username || claim.user.display_name || 'Unknown'}</div>
                    <div>Prize: ${claim.prize.name} (${claim.prize.type})</div>
                    ${claim.payout_tx ? `<div>TX: ${claim.payout_tx}</div>` : ''}
                    <div style="font-size: 12px; color: #666; margin-top: 4px;">${new Date(claim.created_at).toLocaleString()}</div>
                </div>
            `;
            list.appendChild(item);
        });
    } catch (error) {
        console.error('Load claims error:', error);
        alert('Error loading claims');
    }
}

async function loadPrizes() {
    try {
        const response = await fetch('/admin/prizes?token=' + (adminToken || document.getElementById('adminToken').value));
        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        const list = document.getElementById('prizesList');
        list.innerHTML = '';
        
        data.prizes.forEach(prize => {
            const item = document.createElement('div');
            item.className = 'prize-item';
            item.innerHTML = `
                <div class="prize-header">
                    <div>
                        <strong>${prize.name}</strong>
                        <span style="margin-left: 8px; font-size: 12px; color: #666;">${prize.type}</span>
                        <span style="margin-left: 8px; padding: 2px 6px; background: ${prize.is_active ? '#4caf50' : '#999'}; color: #fff; border-radius: 4px; font-size: 11px;">${prize.is_active ? 'Active' : 'Inactive'}</span>
                    </div>
                    <div class="prize-actions">
                        <button class="btn-action btn-edit" onclick="editPrize(${prize.id})">Edit</button>
                    </div>
                </div>
                <div style="margin-top: 8px; font-size: 14px;">
                    <div>Probability: ${(prize.probability * 100).toFixed(4)}%</div>
                    <div style="font-size: 12px; color: #666; margin-top: 4px;">Meta: ${JSON.stringify(prize.meta)}</div>
                </div>
            `;
            list.appendChild(item);
        });
    } catch (error) {
        console.error('Load prizes error:', error);
        alert('Error loading prizes');
    }
}

async function approveClaim(claimId) {
    if (!confirm('Approve this claim?')) return;
    
    try {
        const response = await fetch(`/admin/claim/${claimId}/approve?token=${adminToken || document.getElementById('adminToken').value}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
        const data = await response.json();
        
        if (data.ok) {
            alert('Claim approved');
            loadClaims();
        } else {
            alert(data.error || 'Error approving claim');
        }
    } catch (error) {
        alert('Error approving claim');
    }
}

async function rejectClaim(claimId) {
    if (!confirm('Reject this claim?')) return;
    
    try {
        const response = await fetch(`/admin/claim/${claimId}/reject?token=${adminToken || document.getElementById('adminToken').value}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
        const data = await response.json();
        
        if (data.ok) {
            alert('Claim rejected');
            loadClaims();
        } else {
            alert(data.error || 'Error rejecting claim');
        }
    } catch (error) {
        alert('Error rejecting claim');
    }
}

async function processPayout(claimId) {
    const address = prompt('Enter payout address:');
    if (!address) return;
    
    try {
        const response = await fetch(`/admin/payout/${claimId}?token=${adminToken || document.getElementById('adminToken').value}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({to_address: address})
        });
        const data = await response.json();
        
        if (data.ok) {
            alert(`Payout processed! TX: ${data.tx_hash}`);
            loadClaims();
        } else {
            alert(data.error || 'Error processing payout');
        }
    } catch (error) {
        alert('Error processing payout');
    }
}

function showAddPrizeForm() {
    document.getElementById('prizeModal').style.display = 'flex';
    document.getElementById('prizeForm').reset();
    document.getElementById('prizeId').value = '';
}

function closePrizeModal() {
    document.getElementById('prizeModal').style.display = 'none';
}

async function editPrize(prizeId) {
    try {
        const response = await fetch(`/admin/prizes?token=${adminToken || document.getElementById('adminToken').value}`);
        const data = await response.json();
        const prize = data.prizes.find(p => p.id === prizeId);
        
        if (prize) {
            document.getElementById('prizeId').value = prize.id;
            document.getElementById('prizeName').value = prize.name;
            document.getElementById('prizeType').value = prize.type;
            document.getElementById('prizeProbability').value = prize.probability;
            document.getElementById('prizeMeta').value = JSON.stringify(prize.meta, null, 2);
            document.getElementById('prizeModal').style.display = 'flex';
        }
    } catch (error) {
        alert('Error loading prize');
    }
}

document.getElementById('prizeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        id: document.getElementById('prizeId').value || undefined,
        name: document.getElementById('prizeName').value,
        type: document.getElementById('prizeType').value,
        probability: parseFloat(document.getElementById('prizeProbability').value),
        meta: JSON.parse(document.getElementById('prizeMeta').value || '{}')
    };
    
    try {
        const response = await fetch(`/admin/prize?token=${adminToken || document.getElementById('adminToken').value}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        
        if (data.ok) {
            alert('Prize saved');
            closePrizeModal();
            loadPrizes();
        } else {
            alert(data.error || 'Error saving prize');
        }
    } catch (error) {
        alert('Error saving prize');
    }
});

function switchAdminTab(tab) {
    document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.admin-content').forEach(c => c.style.display = 'none');
    
    if (tab === 'claims') {
        document.querySelectorAll('.admin-tab')[0].classList.add('active');
        document.getElementById('claimsTab').style.display = 'block';
        loadClaims();
    } else if (tab === 'prizes') {
        document.querySelectorAll('.admin-tab')[1].classList.add('active');
        document.getElementById('prizesTab').style.display = 'block';
        loadPrizes();
    } else if (tab === 'audit') {
        document.querySelectorAll('.admin-tab')[2].classList.add('active');
        document.getElementById('auditTab').style.display = 'block';
    }
}

// Load claims on page load
window.addEventListener('load', () => {
    loadClaims();
});

