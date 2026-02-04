"""
IntelliCast LSTM Model Training Script
Trains an LSTM model for network disaster prediction
"""
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import json

print("=" * 60)
print("🧠 IntelliCast LSTM Training System")
print("=" * 60)

# Configuration
WINDOW_SIZE = 50  # timesteps
FEATURES = 3      # load, latency, jitter
EPOCHS = 50
BATCH_SIZE = 32

def generate_training_data(n_samples=2000):
    """Generate synthetic training data for network scenarios"""
    print(f"\n📊 Generating {n_samples} training samples...")
    
    X = []
    y = []
    
    for i in range(n_samples):
        # Generate time series
        if i % 2 == 0:  # Normal scenario
            load = np.random.uniform(10, 60, WINDOW_SIZE)
            latency = 10 + (load ** 1.3) / 100 + np.random.normal(0, 2, WINDOW_SIZE)
            jitter = np.random.uniform(2, 8, WINDOW_SIZE)
            label = 0  # Normal
        else:  # Emergency scenario
            # Gradual increase leading to disaster
            load = np.linspace(40, 95, WINDOW_SIZE) + np.random.normal(0, 5, WINDOW_SIZE)
            latency = 10 + (load ** 1.5) / 80 + np.random.normal(0, 3, WINDOW_SIZE)
            jitter = np.random.uniform(8, 20, WINDOW_SIZE)
            label = 1  # Emergency
        
        # Stack features
        sample = np.column_stack([load, latency, jitter])
        X.append(sample)
        y.append(label)
    
    X = np.array(X)  # Shape: (samples, timesteps, features)
    y = np.array(y)
    
    print(f"✅ Data shape: {X.shape}")
    print(f"   Normal samples: {np.sum(y == 0)}")
    print(f"   Emergency samples: {np.sum(y == 1)}")
    
    return X, y

def build_lstm_model(timesteps, features):
    """Build LSTM model architecture"""
    print("\n🏗️  Building LSTM model architecture...")
    
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(timesteps, features)),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(2, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("✅ Model architecture:")
    model.summary()
    
    return model

def main():
    # Generate training data
    X, y = generate_training_data(n_samples=2000)
    
    # Convert labels to one-hot encoding
    y_onehot = to_categorical(y, 2)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_onehot, test_size=0.2, random_state=42
    )
    
    print(f"\n📦 Training set: {X_train.shape[0]} samples")
    print(f"📦 Test set: {X_test.shape[0]} samples")
    
    # Build model
    model = build_lstm_model(WINDOW_SIZE, FEATURES)
    
    # Train model
    print("\n🚀 Starting training...")
    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate
    print("\n📊 Evaluating model...")
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"✅ Test Accuracy: {accuracy * 100:.2f}%")
    print(f"✅ Test Loss: {loss:.4f}")
    
    # Save model
    model_file = "intelli_lstm_model.h5"
    model.save(model_file)
    print(f"\n💾 Model saved to: {model_file}")
    
    # Save configuration
    config = {
        "window_size": WINDOW_SIZE,
        "features": FEATURES,
        "accuracy": float(accuracy),
        "loss": float(loss),
        "feature_names": ["RRC_Load_pct", "Latency_ms", "Jitter_ms"],
        "class_names": ["Normal", "Emergency"]
    }
    
    with open("model_config.json", "w") as f:
        json.dump(config, f, indent=4)
    
    print("✅ Configuration saved to: model_config.json")
    print("\n" + "=" * 60)
    print("🎉 Training Complete! You can now run lstm_ai_runner.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
