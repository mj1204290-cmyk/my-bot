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
        .card { background: white; padding: 15px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #ffd700; }
        button { background: #fbc02d; color: #000; border: none; padding: 12px; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 5px; }
        .bottom-nav { position: fixed; bottom: 0; width: 100%; display: flex; justify-content: space-around; background: #fff; padding: 10px 0; border-top: 2px solid #fbc02d; z-index: 1000; }
        input, select { width: 90%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 5px; }
    </style>
</head>
<body>

<!-- পেজগুলো এখানে থাকবে -->
<div id="home" class="page active">
    <h2>হোম</h2>
    <div class="card">
        <p>মেইন ব্যালেন্স: <span id="t-balance">0</span> টাকা</p>
        <p>আজকের এড: <span id="t-ad">0</span>/20</p>
    </div>
</div>

<div id="task" class="page">
    <h2>টাস্ক</h2>
    <div class="card">
        <button onclick="watchAd()">এড দেখুন (+৫ টাকা)</button>
    </div>
</div>

<div id="profile" class="page">
    <h2>প্রোফাইল</h2>
    <div class="card" style="background: #2c2c2c; color: white; border-radius: 15px; padding: 20px;">
        <p>আইডি: <span id="p-id">Loading...</span></p>
        <p>ব্যালেন্স: <span id="p-balance">0</span> টাকা</p>
        <button onclick="copyRefLink()" style="background: #444; color: white;">🔗 রেফারেল লিংক কপি</button>
    </div>
</div>

<nav class="bottom-nav">
    <button onclick="showPage('home')">হোম</button>
    <button onclick="showPage('task')">টাস্ক</button>
    <button onclick="showPage('profile')">প্রোফাইল</button>
</nav>

<script>
    // একবারে সব ডাটা লোড করে মেমোরিতে রাখা (এটিই ফাস্ট করার উপায়)
    let userId = localStorage.getItem('userId') || 'JM-' + Math.floor(10000000 + Math.random() * 90000000);
    let balance = parseFloat(localStorage.getItem('balance')) || 0;
    let adCount = parseInt(localStorage.getItem('adCount')) || 0;

    // প্রথমবারের জন্য সেভ করা
    if (!localStorage.getItem('userId')) {
        localStorage.setItem('userId', userId);
        localStorage.setItem('joinDate', new Date().toLocaleDateString());
    }

    function showPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }

    function updateDisplay() {
        document.getElementById('t-balance').innerText = balance;
        document.getElementById('t-ad').innerText = adCount;
        document.getElementById('p-id').innerText = userId;
        document.getElementById('p-balance').innerText = balance;
    }

    function watchAd() {
        if(adCount >= 20) { alert('লিমিট শেষ!'); return; }
        
        // বাটন টিপলে সাথে সাথে আপডেট হবে
        balance += 5;
        adCount++;
        
        // লোকাল স্টোরেজে সেভ করা
        localStorage.setItem('balance', balance);
        localStorage.setItem('adCount', adCount);
        
        updateDisplay();
        alert('সফলভাবে ৫ টাকা যোগ হয়েছে!');
    }

    function copyRefLink() {
        const refLink = "https://t.me/Cabsyab10qq_bot?start=" + userId;
        navigator.clipboard.writeText(refLink);
        alert("লিংক কপি হয়েছে!");
    }

    updateDisplay();
</script>
</body>
</html>
