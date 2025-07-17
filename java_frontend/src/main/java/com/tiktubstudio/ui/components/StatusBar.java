package com.tiktubstudio.ui.components;

import javax.swing.*;
import java.awt.*;

/**
 * Status bar component untuk TikTub Studio
 */
public class StatusBar extends JPanel {
    private JLabel messageLabel;
    private JProgressBar progressBar;
    private JLabel timeLabel;
    
    public StatusBar() {
        initializeComponents();
        setupUI();
    }
    
    private void initializeComponents() {
        messageLabel = new JLabel("Ready");
        progressBar = new JProgressBar();
        timeLabel = new JLabel();
        
        // Setup progress bar
        progressBar.setStringPainted(true);
        progressBar.setVisible(false);
        
        // Update time
        updateTime();
        Timer timer = new Timer(1000, e -> updateTime());
        timer.start();
    }
    
    private void setupUI() {
        setLayout(new BorderLayout());
        setBackground(new Color(45, 45, 48));
        setBorder(BorderFactory.createEmptyBorder(5, 10, 5, 10));
        
        // Left side - message
        messageLabel.setForeground(Color.WHITE);
        messageLabel.setFont(new Font("Arial", Font.PLAIN, 11));
        add(messageLabel, BorderLayout.WEST);
        
        // Center - progress bar
        progressBar.setBackground(new Color(60, 60, 65));
        progressBar.setForeground(new Color(255, 0, 80));
        add(progressBar, BorderLayout.CENTER);
        
        // Right side - time
        timeLabel.setForeground(new Color(180, 180, 180));
        timeLabel.setFont(new Font("Arial", Font.PLAIN, 11));
        add(timeLabel, BorderLayout.EAST);
    }
    
    public void setMessage(String message) {
        SwingUtilities.invokeLater(() -> {
            messageLabel.setText(message);
        });
    }
    
    public void setProgress(String message, int progress) {
        SwingUtilities.invokeLater(() -> {
            messageLabel.setText(message);
            progressBar.setValue(progress);
            progressBar.setString(progress + "%");
            progressBar.setVisible(true);
        });
    }
    
    public void hideProgress() {
        SwingUtilities.invokeLater(() -> {
            progressBar.setVisible(false);
        });
    }
    
    private void updateTime() {
        SwingUtilities.invokeLater(() -> {
            timeLabel.setText(new java.text.SimpleDateFormat("HH:mm:ss").format(new java.util.Date()));
        });
    }
}