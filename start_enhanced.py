#!/usr/bin/env python3
"""
🎬 TikTub Studio Enhanced - Startup Script
AI-Powered Short Video Creator with Duolingo-inspired UI
"""

import os
import sys
import subprocess
import time
import json
import platform
from pathlib import Path

def print_header():
    """Print the application header"""
    print("=" * 60)
    print("🎬 TikTub Studio Enhanced - AI Video Creator")
    print("Transform your long videos into viral shorts!")
    print("=" * 60)
    print()

def print_colored(text, color='white'):
    """Print colored text"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[0m'
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['end']}")

def check_system():
    """Check system requirements"""
    print_colored("🔍 Checking system requirements...", 'cyan')
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print_colored(f"✅ Python {python_version.major}.{python_version.minor} - OK", 'green')
    else:
        print_colored(f"❌ Python {python_version.major}.{python_version.minor} - Need 3.8+", 'red')
        return False
    
    # Check Java
    try:
        java_result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if java_result.returncode == 0:
            print_colored("✅ Java - OK", 'green')
        else:
            print_colored("❌ Java not found", 'red')
            print_colored("   Install Java 11+ from: https://adoptium.net/", 'yellow')
    except FileNotFoundError:
        print_colored("❌ Java not found", 'red')
        print_colored("   Install Java 11+ from: https://adoptium.net/", 'yellow')
    
    # Check available memory
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        if memory_gb >= 8:
            print_colored(f"✅ RAM: {memory_gb:.1f}GB - OK", 'green')
        else:
            print_colored(f"⚠️  RAM: {memory_gb:.1f}GB - Recommended 8GB+", 'yellow')
    except ImportError:
        print_colored("ℹ️  Memory check skipped (psutil not available)", 'blue')
    
    print()
    return True

def create_demo_mode():
    """Create demo mode with mock data"""
    print_colored("🎭 Creating demo mode...", 'cyan')
    
    # Create demo configuration
    demo_config = {
        "demo_mode": True,
        "features": {
            "ai_analysis": True,
            "effect_generation": True,
            "subtitle_generation": True,
            "video_processing": True
        },
        "ui": {
            "theme": "duolingo_inspired",
            "animations": True,
            "modern_cards": True
        },
        "mock_processing_time": 5  # seconds
    }
    
    with open('demo_config.json', 'w') as f:
        json.dump(demo_config, f, indent=2)
    
    print_colored("✅ Demo mode configured", 'green')
    print()

def show_features():
    """Show application features"""
    print_colored("✨ Enhanced Features:", 'purple')
    print("🤖 Advanced AI Video Analysis")
    print("   • YOLO object detection")
    print("   • Face recognition and tracking")
    print("   • Motion analysis with optical flow")
    print("   • Audio quality assessment")
    print("   • Technical quality scoring")
    print()
    
    print("🎨 Professional Effects System")
    print("   • AI-driven color grading")
    print("   • Dynamic transitions")
    print("   • Theme-aware visual effects")
    print("   • Animated text and subtitles")
    print()
    
    print("📱 Modern Duolingo-Inspired UI")
    print("   • Card-based design")
    print("   • Smooth animations")
    print("   • Drag-and-drop upload")
    print("   • Real-time progress tracking")
    print()
    
    print("🎯 Smart Processing")
    print("   • 5 effect themes (Energetic, Calm, Educational, etc.)")
    print("   • Automatic best moment detection")
    print("   • Multi-platform optimization")
    print("   • Professional subtitle generation")
    print()

def install_instructions():
    """Show installation instructions"""
    print_colored("📦 Installation Instructions:", 'yellow')
    print()
    
    print_colored("1. Install Dependencies:", 'cyan')
    if platform.system() == "Windows":
        print("   pip install --user opencv-python torch torchvision")
        print("   pip install --user moviepy whisper transformers")
        print("   pip install --user ultralytics face-recognition")
    else:
        print("   python3 -m pip install --user opencv-python torch torchvision")
        print("   python3 -m pip install --user moviepy whisper transformers") 
        print("   python3 -m pip install --user ultralytics face-recognition")
    print()
    
    print_colored("2. Java Setup:", 'cyan')
    print("   • Download Java 11+ from: https://adoptium.net/")
    print("   • Install Maven from: https://maven.apache.org/")
    print()
    
    print_colored("3. GPU Acceleration (Optional):", 'cyan')
    print("   • Install CUDA Toolkit for NVIDIA GPUs")
    print("   • Install PyTorch with CUDA support")
    print()

def start_demo_ui():
    """Start the demo UI"""
    print_colored("🚀 Starting TikTub Studio Enhanced...", 'green')
    print()
    
    try:
        # Try to start the Java UI in demo mode
        java_demo_code = '''
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class TikTubStudioDemo {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            createAndShowGUI();
        });
    }
    
    private static void createAndShowGUI() {
        JFrame frame = new JFrame("TikTub Studio Enhanced - Demo Mode");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(1200, 800);
        frame.setLocationRelativeTo(null);
        
        // Create main panel
        JPanel mainPanel = new JPanel(new BorderLayout());
        mainPanel.setBackground(new Color(248, 250, 252));
        
        // Header
        JPanel header = new JPanel(new FlowLayout());
        header.setBackground(Color.WHITE);
        header.setBorder(BorderFactory.createMatteBorder(0, 0, 1, 0, new Color(229, 232, 235)));
        
        JLabel logo = new JLabel("🎬 TikTub Studio Enhanced");
        logo.setFont(new Font("Segoe UI", Font.BOLD, 24));
        logo.setForeground(new Color(59, 72, 80));
        header.add(logo);
        
        // Demo content
        JPanel content = new JPanel();
        content.setLayout(new BoxLayout(content, BoxLayout.Y_AXIS));
        content.setBackground(new Color(248, 250, 252));
        content.setBorder(BorderFactory.createEmptyBorder(50, 50, 50, 50));
        
        // Welcome message
        JLabel welcome = new JLabel("<html><center><h1>Welcome to TikTub Studio Enhanced!</h1><br>" +
            "<h3>AI-Powered Short Video Creator</h3><br>" +
            "This is a demo showcasing the modern Duolingo-inspired UI<br><br>" +
            "<b>Enhanced Features:</b><br>" +
            "🤖 Advanced AI Video Analysis<br>" +
            "🎨 Professional Effects System<br>" +
            "📱 Modern Card-Based UI<br>" +
            "🎯 Smart Content Detection<br><br>" +
            "To use the full application, please install the dependencies<br>" +
            "as shown in the setup guide.</center></html>");
        welcome.setHorizontalAlignment(SwingConstants.CENTER);
        welcome.setFont(new Font("Segoe UI", Font.PLAIN, 16));
        welcome.setForeground(new Color(59, 72, 80));
        
        // Demo button
        JButton demoButton = new JButton("View Setup Guide");
        demoButton.setFont(new Font("Segoe UI", Font.BOLD, 14));
        demoButton.setBackground(new Color(88, 204, 2));
        demoButton.setForeground(Color.WHITE);
        demoButton.setFocusPainted(false);
        demoButton.setBorderPainted(false);
        demoButton.setPreferredSize(new Dimension(200, 40));
        demoButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    Desktop.getDesktop().open(new java.io.File("SETUP_GUIDE.md"));
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(frame, 
                        "Please check SETUP_GUIDE.md for installation instructions");
                }
            }
        });
        
        content.add(welcome);
        content.add(Box.createVerticalStrut(30));
        
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setOpaque(false);
        buttonPanel.add(demoButton);
        content.add(buttonPanel);
        
        mainPanel.add(header, BorderLayout.NORTH);
        mainPanel.add(content, BorderLayout.CENTER);
        
        frame.add(mainPanel);
        frame.setVisible(true);
    }
}
'''
        
        # Save and compile Java demo
        with open('TikTubStudioDemo.java', 'w') as f:
            f.write(java_demo_code)
        
        print_colored("Compiling demo UI...", 'cyan')
        compile_result = subprocess.run(['javac', 'TikTubStudioDemo.java'], 
                                      capture_output=True, text=True)
        
        if compile_result.returncode == 0:
            print_colored("Starting demo UI...", 'green')
            subprocess.run(['java', 'TikTubStudioDemo'])
        else:
            print_colored("Java compilation failed. Showing text-based demo.", 'yellow')
            show_text_demo()
            
    except Exception as e:
        print_colored(f"Could not start GUI demo: {e}", 'yellow')
        show_text_demo()

def show_text_demo():
    """Show text-based demo"""
    print_colored("📺 TikTub Studio Enhanced - Text Demo", 'cyan')
    print()
    
    demo_steps = [
        "1. 📤 Upload Video: Drag & drop your video file",
        "2. 🤖 AI Analysis: Advanced algorithms analyze content",  
        "3. 🎨 Smart Effects: AI applies perfect theme-based effects",
        "4. 📝 Auto Subtitles: Whisper AI generates accurate captions",
        "5. 🎬 Export: Download optimized short videos"
    ]
    
    for step in demo_steps:
        print_colored(step, 'green')
        time.sleep(1)
    
    print()
    print_colored("🎯 The full application features:", 'purple')
    print("• Modern Duolingo-inspired UI with smooth animations")
    print("• Advanced AI scene detection with YOLO and face recognition")
    print("• Professional color grading and cinematic effects")
    print("• Real-time progress tracking and preview")
    print("• Multi-platform output (TikTok, YouTube Shorts, Instagram)")
    print()

def main():
    """Main function"""
    print_header()
    
    if not check_system():
        print_colored("Please install missing requirements and try again.", 'red')
        return
    
    show_features()
    
    # Ask user what they want to do
    print_colored("What would you like to do?", 'cyan')
    print("1. 🚀 Start Demo UI")
    print("2. 📖 View Installation Guide") 
    print("3. 🎭 Show Text Demo")
    print("4. ❌ Exit")
    print()
    
    try:
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            create_demo_mode()
            start_demo_ui()
        elif choice == "2":
            install_instructions()
            print_colored("\nSee SETUP_GUIDE.md for complete instructions!", 'green')
        elif choice == "3":
            show_text_demo()
        elif choice == "4":
            print_colored("Thanks for trying TikTub Studio Enhanced! 🎬", 'green')
        else:
            print_colored("Invalid choice. Showing text demo.", 'yellow')
            show_text_demo()
            
    except KeyboardInterrupt:
        print_colored("\nGoodbye! 👋", 'green')
    except Exception as e:
        print_colored(f"Error: {e}", 'red')

if __name__ == "__main__":
    main()