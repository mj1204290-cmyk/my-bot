<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jm Android Earning</title>
    <style>
        body { font-family: sans-serif; background: #fffde7; margin: 0; padding-bottom: 70px; }
        .page { display: none; padding: 15px; }
        .active { display: block; }
        .card { background: white; padding: 15px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border: 1px solid #ffd700; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        table, th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        button { background: #fbc02d; color: #000; border: none; padding: 12px; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 5px; }
        .bottom-nav { position: fixed; bottom: 0; width: 100%; display: flex; justify-content: space-around; background: #fff; padding: 10px 0; border-top: 2px solid #fbc02d; z-index: 1000; }
        .bottom-nav button { width: auto; font-size: 12px; padding: 5px 8px; }
        input, select { width: 90%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; }
    </style>
</head>
<body>

<div id="home" class="page active">
    <h2>হোম</h2>
    <div class="card">
        <table>
            <tr><th>তথ্য</th><th>বিবরণ</th></tr>
            <tr><td>মেইন ব্যালেন্স</td><td id="t-balance">0 টাকা</td></tr>
            <tr><td>আজকের এড</td><td id="t-ad">0/20</td></tr>
            <tr><td>রেফারেল সংখ্যা</td><td id="t-ref">0 জন</td></tr>
        </table>
    </div>
</div>

<div id="task" class="page">
    <h2>টাস্ক</h2>
    <div class="card">
        <p>আজকের এড: <span id="ad-count">0</span>/20</p>
        <button onclick="watchAd()">এড দেখুন (+৫ টাকা)</button>
        <hr>
        <button onclick="joinGroup('https://t.me/king3gh')">১ম গ্রুপে জয়েন করুন (+৫ টাকা)</button>
        <button onclick="joinGroup('https://t.me/sih3gh2ns')">২য় গ্রুপে জয়েন করুন (+৫ টাকা)</button>
    </div>
</div>

<div id="withdraw" class="page">
    <h2>উইথড্র</h2>
    <div class="card">
        <h3>উইথড্র শর্তাবলী</h3>
        <p style="font-size: 13px;">• ন্যূনতম ৫০০ টাকা<br>• ১৫টি রেফারেল<br>• ১০টি এড দেখা</p>
    </div>
    <div class="card">
        <select id="method"><option value="bKash">বিকাশ</option><option value="Nagad">নগদ</option></select>
        <input type="number" id="w-amount" placeholder="পরিমাণ (কমপক্ষে ৫০০)">
        <input type="text" id="w-number" placeholder="আপনার নাম্বার">
        <button onclick="withdraw()">উইথড্র পাঠান</button>
        <h3>আপনার উইথড্র রিকোয়েস্ট:</h3>
        <ul id="w-list"></ul>
    </div>
</div>

<div id="profile" class="page">
    <h2>প্রোফাইল</h2>
    <div class="card" style="text-align: center; background: #2c2c2c; color: white; border-radius: 20px;">
        <div style="font-size: 60px; margin-bottom: 10px;">👤</div>
        <h3 id="p-name" style="margin: 5px 0;">User</h3>
        <p style="margin: 0; color: #ccc;">আইডি: <span id="p-id">Loading...</span></p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px;">
            <div style="background: #333; padding: 10px; border-radius: 15px;"><p style="margin:0;">💰 <span id="p-balance">0</span> টাকা</p></div>
            <div style="background: #333; padding: 10px; border-radius: 15px;"><p style="margin:0;">👁️ <span id="p-ad">0</span> এড</p></div>
            <div style="background: #333; padding: 10px; border-radius: 15px;"><p style="margin:0;">👥 <span id="p-ref">0</span> রেফারেল</p></div>
            <div style="background: #333; padding: 10px; border-radius: 15px;"><p style="margin:0;">📅 <span id="join-date">Loading...</span></p></div>
        </div>
        <div style="margin-top: 20px; text-align: left;">
            <button onclick="copyRefLink()" style="background: #444; color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; cursor: pointer;">🔗 রেফারেল লিংক কপি</button>
        </div>
    </div>
</div>

<nav class="bottom-nav">
    <button onclick="showPage('home')">হোম</button>
    <button onclick="showPage('task')">টাস্ক</button>
    <button onclick="showPage('withdraw')">উইথড্র</button>
    <button onclick="showPage('profile')">প্রোফাইল</button>
</nav>

<script>
    // অটোমেটিক ডাটা জেনারেশন
    if (!localStorage.getItem('userId')) {
        localStorage.setItem('userId', 'JM-' + Math.floor(10000000 + Math.random() * 90000000));
        localStorage.setItem('joinDate', new Date().toLocaleDateString());
    }

    // ভ্যারিয়েবল সেটআপ
    let balance = parseFloat(localStorage.getItem('balance')) || 0;
    let adCount = parseInt(localStorage.getItem('adCount')) || 0;
    let refCount = parseInt(localStorage.getItem('refCount')) || 0;
    let wList = JSON.parse(localStorage.getItem('wList')) || [];
    let userId = localStorage.getItem('userId');
    let joinDate = localStorage.getItem('joinDate');

    function showPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }

    function updateDisplay() {
        document.getElementById('t-balance').innerText = balance + " টাকা";
        document.getElementById('t-ad').innerText = adCount + "/20";
        document.getElementById('t-ref').innerText = refCount + " জন";
        document.getElementById('ad-count').innerText = adCount;
        
        document.getElementById('p-id').innerText = userId;
        document.getElementById('p-balance').innerText = balance;
        document.getElementById('p-ad').innerText = adCount;
        document.getElementById('p-ref').innerText = refCount;
        document.getElementById('join-date').innerText = joinDate;
        
        const list = document.getElementById('w-list');
        list.innerHTML = wList.map(item => `<li>${item.date}: ${item.amount} টাকা - ${item.status}</li>`).join('');
    }

    function watchAd() {
        if(adCount >= 20) { alert('আজকের লিমিট শেষ!'); return; }
        alert('এড চলছে... ৩০ সেকেন্ড পর ওকে করুন');
        setTimeout(() => {
            balance += 5;
            adCount++;
            localStorage.setItem('balance', balance);
            localStorage.setItem('adCount', adCount);
            updateDisplay();
        }, 3000); 
    }

    // আপনার বটের ইউআরএল দিয়ে আপডেট করা ফাংশন
    function copyRefLink() {
        const refLink = "https://t.me/Cabsyab10qq_bot?start=" + userId;
        navigator.clipboard.writeText(refLink).then(() => {
            alert("আপনার রেফারেল লিংক কপি হয়েছে: " + refLink);
        });
    }

    function joinGroup(url) {
        window.open(url, '_blank');
        alert("গ্রুপে জয়েন করার জন্য ধন্যবাদ!");
    }

    function withdraw() {
        let amount = parseFloat(document.getElementById('w-amount').value);
        if(amount >= 500 && balance >= amount) {
            balance -= amount;
            wList.push({date: new Date().toLocaleDateString(), amount, status: 'Pending'});
            localStorage.setItem('balance', balance);
            localStorage.setItem('wList', JSON.stringify(wList));
            updateDisplay();
            alert('উইথড্র সফল হয়েছে!');
        } else {
            alert('শর্ত পূরণ হয়নি!');
        }
    }

    updateDisplay();
</script>
</body>
</html>
