package com.tiktubstudio.ui.panels;

import com.tiktubstudio.api.ApiClient;
import com.tiktubstudio.ui.MainWindow;

import javax.swing.*;
import java.awt.*;

/**
 * Panel untuk konfigurasi dan processing video
 */
public class ProcessingPanel extends JPanel {
    private ApiClient apiClient;
    private MainWindow mainWindow;
    private boolean isProcessing = false;
    
    // UI Components
    private JComboBox<String> platformCombo;
    private JSpinner segmentSpinner;
    private JComboBox<String> themeCombo;
    private JComboBox<String> languageCombo;
    private JButton startButton;
    private JProgressBar progressBar;
    private JTextArea logArea;
    
    public ProcessingPanel(ApiClient apiClient, MainWindow mainWindow) {
        this.apiClient = apiClient;
        this.mainWindow = mainWindow;
        initializeComponents();
        setupUI();
    }
    
    private void initializeComponents() {
        platformCombo = new JComboBox<>(new String[]{"TikTok", "YouTube Shorts", "Instagram Reels", "Custom"});
        segmentSpinner = new JSpinner(new SpinnerNumberModel(3, 1, 10, 1));
        themeCombo = new JComboBox<>(new String[]{"Auto", "Energetic", "Calm", "Educational", "Entertainment", "Dramatic"});
        languageCombo = new JComboBox<>(new String[]{"Auto", "Indonesian", "English"});
        startButton = new JButton("🚀 Start Processing");
        progressBar = new JProgressBar(0, 100);
        logArea = new JTextArea();
    }
    
    private void setupUI() {
        setLayout(new BorderLayout());
        setBackground(new Color(32, 32, 35));
        setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        
        // Configuration panel
        JPanel configPanel = createConfigPanel();
        add(configPanel, BorderLayout.NORTH);
        
        // Progress panel
        JPanel progressPanel = createProgressPanel();
        add(progressPanel, BorderLayout.CENTER);
        
        // Log panel
        JPanel logPanel = createLogPanel();
        add(logPanel, BorderLayout.SOUTH);
    }
    
    private JPanel createConfigPanel() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBackground(new Color(32, 32, 35));
        panel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(255, 0, 80)), 
            "Configuration", 
            0, 0, 
            new Font("Arial", Font.BOLD, 14), 
            Color.WHITE
        ));
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.anchor = GridBagConstraints.WEST;
        
        // Platform
        gbc.gridx = 0; gbc.gridy = 0;
        panel.add(createLabel("Target Platform:"), gbc);
        gbc.gridx = 1;
        styleComboBox(platformCombo);
        panel.add(platformCombo, gbc);
        
        // Segments
        gbc.gridx = 0; gbc.gridy = 1;
        panel.add(createLabel("Number of Segments:"), gbc);
        gbc.gridx = 1;
        styleSpinner(segmentSpinner);
        panel.add(segmentSpinner, gbc);
        
        // Theme
        gbc.gridx = 0; gbc.gridy = 2;
        panel.add(createLabel("Effect Theme:"), gbc);
        gbc.gridx = 1;
        styleComboBox(themeCombo);
        panel.add(themeCombo, gbc);
        
        // Language
        gbc.gridx = 0; gbc.gridy = 3;
        panel.add(createLabel("Subtitle Language:"), gbc);
        gbc.gridx = 1;
        styleComboBox(languageCombo);
        panel.add(languageCombo, gbc);
        
        // Start button
        gbc.gridx = 0; gbc.gridy = 4; gbc.gridwidth = 2; gbc.fill = GridBagConstraints.HORIZONTAL;
        styleButton(startButton);
        startButton.addActionListener(e -> startProcessing());
        panel.add(startButton, gbc);
        
        return panel;
    }
    
    private JPanel createProgressPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(new Color(32, 32, 35));
        panel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(255, 0, 80)), 
            "Progress", 
            0, 0, 
            new Font("Arial", Font.BOLD, 14), 
            Color.WHITE
        ));
        
        // Progress bar
        progressBar.setStringPainted(true);
        progressBar.setString("Ready to start");
        progressBar.setBackground(new Color(45, 45, 48));
        progressBar.setForeground(new Color(255, 0, 80));
        progressBar.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        panel.add(progressBar, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel createLogPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(new Color(32, 32, 35));
        panel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(255, 0, 80)), 
            "Processing Log", 
            0, 0, 
            new Font("Arial", Font.BOLD, 14), 
            Color.WHITE
        ));
        
        logArea.setEditable(false);
        logArea.setBackground(new Color(25, 25, 28));
        logArea.setForeground(new Color(200, 200, 200));
        logArea.setFont(new Font("Consolas", Font.PLAIN, 11));
        logArea.setText("Ready to process video...\n");
        
        JScrollPane scrollPane = new JScrollPane(logArea);
        scrollPane.setPreferredSize(new Dimension(0, 150));
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JLabel createLabel(String text) {
        JLabel label = new JLabel(text);
        label.setForeground(Color.WHITE);
        label.setFont(new Font("Arial", Font.PLAIN, 12));
        return label;
    }
    
    private void styleComboBox(JComboBox<String> combo) {
        combo.setBackground(new Color(45, 45, 48));
        combo.setForeground(Color.WHITE);
        combo.setFont(new Font("Arial", Font.PLAIN, 12));
        combo.setFocusable(false);
    }
    
    private void styleSpinner(JSpinner spinner) {
        spinner.setBackground(new Color(45, 45, 48));
        spinner.setForeground(Color.WHITE);
        spinner.setFont(new Font("Arial", Font.PLAIN, 12));
        
        // Style spinner editor
        JSpinner.DefaultEditor editor = (JSpinner.DefaultEditor) spinner.getEditor();
        editor.getTextField().setBackground(new Color(45, 45, 48));
        editor.getTextField().setForeground(Color.WHITE);
        editor.getTextField().setBorder(BorderFactory.createEmptyBorder());
    }
    
    private void styleButton(JButton button) {
        button.setBackground(new Color(255, 0, 80));
        button.setForeground(Color.WHITE);
        button.setFont(new Font("Arial", Font.BOLD, 14));
        button.setFocusPainted(false);
        button.setBorder(BorderFactory.createEmptyBorder(10, 20, 10, 20));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        
        // Hover effect
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                if (button.isEnabled()) {
                    button.setBackground(new Color(230, 0, 70));
                }
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                if (button.isEnabled()) {
                    button.setBackground(new Color(255, 0, 80));
                }
            }
        });
    }
    
    private void startProcessing() {
        if (isProcessing) {
            return;
        }
        
        // Check if file is selected
        if (mainWindow.getUploadPanel().getSelectedFile() == null) {
            JOptionPane.showMessageDialog(this, 
                "Please select a video file first.", 
                "No File Selected", 
                JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        // Start processing simulation
        isProcessing = true;
        startButton.setEnabled(false);
        startButton.setText("⏳ Processing...");
        
        appendLog("Starting video processing...");
        appendLog("Platform: " + platformCombo.getSelectedItem());
        appendLog("Segments: " + segmentSpinner.getValue());
        appendLog("Theme: " + themeCombo.getSelectedItem());
        appendLog("Language: " + languageCombo.getSelectedItem());
        
        // Simulate processing with progress updates
        SwingWorker<Void, Integer> worker = new SwingWorker<Void, Integer>() {
            @Override
            protected Void doInBackground() throws Exception {
                String[] steps = {
                    "Uploading video...",
                    "Analyzing content...", 
                    "Generating subtitles...",
                    "Applying effects...",
                    "Rendering segments...",
                    "Finalizing videos..."
                };
                
                for (int i = 0; i < steps.length; i++) {
                    Thread.sleep(2000); // Simulate processing time
                    appendLog(steps[i]);
                    publish((i + 1) * 100 / steps.length);
                }
                
                return null;
            }
            
            @Override
            protected void process(java.util.List<Integer> chunks) {
                int progress = chunks.get(chunks.size() - 1);
                progressBar.setValue(progress);
                progressBar.setString(progress + "%");
            }
            
            @Override
            protected void done() {
                appendLog("Processing completed successfully!");
                progressBar.setString("Completed");
                
                isProcessing = false;
                startButton.setEnabled(true);
                startButton.setText("🚀 Start Processing");
                
                // Switch to results tab
                mainWindow.switchToResultsTab();
            }
        };
        
        worker.execute();
    }
    
    private void appendLog(String message) {
        SwingUtilities.invokeLater(() -> {
            logArea.append("[" + new java.text.SimpleDateFormat("HH:mm:ss").format(new java.util.Date()) + "] " + message + "\n");
            logArea.setCaretPosition(logArea.getDocument().getLength());
        });
    }
    
    public boolean isProcessing() {
        return isProcessing;
    }
}