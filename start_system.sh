

echo "=========================================="
echo "🧠 IntelliCast System Launcher"
echo "=========================================="
echo ""

if [ ! -f "intelli_lstm_model.h5" ]; then
    echo "❌ LSTM model not found!"
    echo "📚 Please train the model first:"
    echo "   python3 train_lstm.py"
    echo ""
    exit 1
fi

echo "✅ Model found: intelli_lstm_model.h5"
echo ""


echo "🔍 Checking dependencies..."
python3 -c "import tensorflow; import numpy; import streamlit; import plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies!"
    echo "📚 Please install requirements:"
    echo "   pip3 install -r requirements.txt"
    echo ""
    exit 1
fi

echo "✅ All dependencies installed"
echo ""

echo "=========================================="
echo "🚀 Starting IntelliCast System"
echo "=========================================="
echo ""
echo "This will open 4 terminal windows:"
echo "  1️⃣  Network Telemetry Simulator"
echo "  2️⃣  AI-Native Orchestrator"
echo "  3️⃣  Streamlit Dashboard"
echo "  4️⃣  LSTM AI Brain"
echo ""
echo "Press Ctrl+C in each terminal to stop"
echo ""


launch_terminal() {
    local cmd="$1"
    local title="$2"
    
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal --title="$title" -- bash -c "$cmd; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -title "$title" -e "$cmd; bash" &
    elif command -v konsole &> /dev/null; then
        konsole --title "$title" -e "$cmd; bash" &
    else
        echo "⚠️  No terminal emulator found"
        echo "Please open 4 terminals manually and run:"
        echo ""
        echo "Terminal 1: python3 network_scenario.py"
        echo "Terminal 2: python3 orchestrator.py"
        echo "Terminal 3: streamlit run dashboard.py"
        echo "Terminal 4: python3 lstm_ai_runner.py"
        exit 1
    fi
}


echo "🔧 Launching Terminal 1: Network Simulator..."
launch_terminal "python3 network_scenario.py" "IntelliCast: Network Simulator"
sleep 2

echo "🔧 Launching Terminal 2: Orchestrator..."
launch_terminal "python3 orchestrator.py" "IntelliCast: Orchestrator"
sleep 2

echo "🔧 Launching Terminal 3: Dashboard..."
launch_terminal "streamlit run dashboard.py" "IntelliCast: Dashboard"
sleep 2

echo "🔧 Launching Terminal 4: LSTM AI Brain..."
launch_terminal "python3 lstm_ai_runner.py" "IntelliCast: AI Brain"
sleep 2

echo ""
echo "=========================================="
echo "✅ All components launched!"
echo "=========================================="
echo ""
echo "📊 Open your browser to: http://localhost:8501"
echo ""
echo "To stop the system:"
echo "  Press Ctrl+C in each terminal window"
echo ""
echo "=========================================="
