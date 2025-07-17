package com.tiktubstudio;

import com.formdev.flatlaf.FlatDarkLaf;
import com.tiktubstudio.ui.MainWindow;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.swing.*;
import java.awt.*;

/**
 * Main application class untuk TikTub Studio
 */
public class TikTubStudioApp {
    private static final Logger logger = LoggerFactory.getLogger(TikTubStudioApp.class);
    
    public static void main(String[] args) {
        // Set system properties untuk better UI
        System.setProperty("apple.laf.useScreenMenuBar", "true");
        System.setProperty("apple.awt.application.name", "TikTub Studio");
        System.setProperty("file.encoding", "UTF-8");
        
        // Initialize FlatLaf (Modern UI)
        try {
            UIManager.setLookAndFeel(new FlatDarkLaf());
            
            // Custom colors untuk TikTub Studio theme
            UIManager.put("Button.arc", 10);
            UIManager.put("Component.arc", 10);
            UIManager.put("ProgressBar.arc", 10);
            UIManager.put("TextComponent.arc", 10);
            
            // Custom color scheme
            UIManager.put("accentColor", new Color(255, 0, 80)); // TikTok pink
            UIManager.put("Button.background", new Color(45, 45, 48));
            UIManager.put("Button.hoverBackground", new Color(60, 60, 65));
            UIManager.put("Panel.background", new Color(32, 32, 35));
            UIManager.put("TextField.background", new Color(45, 45, 48));
            
        } catch (Exception e) {
            logger.error("Failed to initialize FlatLaf", e);
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeel());
            } catch (Exception ex) {
                logger.error("Failed to set system look and feel", ex);
            }
        }
        
        // Enable antialiasing
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        
        // Set up uncaught exception handler
        Thread.setDefaultUncaughtExceptionHandler((thread, exception) -> {
            logger.error("Uncaught exception in thread " + thread.getName(), exception);
            
            SwingUtilities.invokeLater(() -> {
                JOptionPane.showMessageDialog(
                    null,
                    "Terjadi kesalahan yang tidak terduga:\n" + exception.getMessage(),
                    "Error",
                    JOptionPane.ERROR_MESSAGE
                );
            });
        });
        
        // Start application on Event Dispatch Thread
        SwingUtilities.invokeLater(() -> {
            try {
                logger.info("Starting TikTub Studio Application");
                
                // Show splash screen
                showSplashScreen();
                
                // Create and show main window
                MainWindow mainWindow = new MainWindow();
                mainWindow.setVisible(true);
                
                logger.info("TikTub Studio Application started successfully");
                
            } catch (Exception e) {
                logger.error("Failed to start application", e);
                JOptionPane.showMessageDialog(
                    null,
                    "Gagal memulai aplikasi: " + e.getMessage(),
                    "Error",
                    JOptionPane.ERROR_MESSAGE
                );
                System.exit(1);
            }
        });
    }
    
    private static void showSplashScreen() {
        JWindow splash = new JWindow();
        splash.setSize(400, 250);
        splash.setLocationRelativeTo(null);
        
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(new Color(32, 32, 35));
        panel.setBorder(BorderFactory.createLineBorder(new Color(255, 0, 80), 2));
        
        // Logo/Title
        JLabel titleLabel = new JLabel("TikTub Studio", JLabel.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 28));
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setBorder(BorderFactory.createEmptyBorder(40, 20, 20, 20));
        
        // Version info
        JLabel versionLabel = new JLabel("v1.0.0 - AI-Powered Short Video Creator", JLabel.CENTER);
        versionLabel.setFont(new Font("Arial", Font.PLAIN, 12));
        versionLabel.setForeground(new Color(180, 180, 180));
        
        // Loading animation
        JProgressBar progressBar = new JProgressBar();
        progressBar.setIndeterminate(true);
        progressBar.setBackground(new Color(45, 45, 48));
        progressBar.setForeground(new Color(255, 0, 80));
        progressBar.setBorder(BorderFactory.createEmptyBorder(10, 40, 20, 40));
        
        JLabel loadingLabel = new JLabel("Memuat aplikasi...", JLabel.CENTER);
        loadingLabel.setFont(new Font("Arial", Font.PLAIN, 11));
        loadingLabel.setForeground(new Color(160, 160, 160));
        loadingLabel.setBorder(BorderFactory.createEmptyBorder(0, 20, 10, 20));
        
        panel.add(titleLabel, BorderLayout.NORTH);
        panel.add(versionLabel, BorderLayout.CENTER);
        
        JPanel bottomPanel = new JPanel(new BorderLayout());
        bottomPanel.setBackground(new Color(32, 32, 35));
        bottomPanel.add(progressBar, BorderLayout.CENTER);
        bottomPanel.add(loadingLabel, BorderLayout.SOUTH);
        
        panel.add(bottomPanel, BorderLayout.SOUTH);
        
        splash.add(panel);
        splash.setVisible(true);
        
        // Hide splash after delay
        Timer timer = new Timer(2000, e -> splash.dispose());
        timer.setRepeats(false);
        timer.start();
    }
}