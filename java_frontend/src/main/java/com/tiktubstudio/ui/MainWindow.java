package com.tiktubstudio.ui;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.tiktubstudio.api.ApiClient;
import com.tiktubstudio.ui.components.*;
import com.tiktubstudio.ui.panels.*;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.util.concurrent.CompletableFuture;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Enhanced Main Window dengan Duolingo-inspired UI design
 * Featuring modern cards, smooth animations, dan intuitive user experience
 */
public class MainWindow extends JFrame {
    private static final Logger logger = LoggerFactory.getLogger(MainWindow.class);
    
    // UI Components
    private JPanel mainContentPanel;
    private JPanel sidebarPanel;
    private JPanel headerPanel;
    private JPanel statusPanel;
    
    // Card Panels
    private VideoUploadCard uploadCard;
    private ProcessingOptionsCard optionsCard;
    private ProgressCard progressCard;
    private ResultsCard resultsCard;
    
    // Status Components
    private JLabel statusLabel;
    private JProgressBar globalProgressBar;
    private ModernButton processButton;
    
    // Data
    private File selectedVideoFile;
    private ApiClient apiClient;
    private boolean isProcessing = false;
    
    // UI Constants - Duolingo-inspired
    private static final Color PRIMARY_GREEN = new Color(88, 204, 2);
    private static final Color SECONDARY_BLUE = new Color(28, 176, 246);
    private static final Color ACCENT_YELLOW = new Color(255, 205, 0);
    private static final Color DANGER_RED = new Color(255, 75, 75);
    private static final Color BACKGROUND_LIGHT = new Color(248, 250, 252);
    private static final Color CARD_BACKGROUND = new Color(255, 255, 255);
    private static final Color TEXT_PRIMARY = new Color(59, 72, 80);
    private static final Color TEXT_SECONDARY = new Color(119, 137, 151);
    private static final Color BORDER_COLOR = new Color(229, 232, 235);
    
    private static final Font TITLE_FONT = new Font("Segoe UI", Font.BOLD, 24);
    private static final Font SUBTITLE_FONT = new Font("Segoe UI", Font.PLAIN, 16);
    private static final Font BODY_FONT = new Font("Segoe UI", Font.PLAIN, 14);
    private static final Font CAPTION_FONT = new Font("Segoe UI", Font.PLAIN, 12);

    public MainWindow() {
        super("TikTub Studio - AI Video Creator");
        
        this.apiClient = new ApiClient();
        
        initializeWindow();
        createLayout();
        setupEventHandlers();
        
        // Show welcome animation
        showWelcomeAnimation();
        
        logger.info("TikTub Studio Main Window initialized successfully");
    }

    private void initializeWindow() {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1400, 900);
        setMinimumSize(new Dimension(1200, 800));
        setLocationRelativeTo(null);
        
        // Set modern window appearance
        getRootPane().setBorder(new EmptyBorder(0, 0, 0, 0));
        setBackground(BACKGROUND_LIGHT);
        
        // Set window icon
        try {
            // You would load your app icon here
            // setIconImage(ImageIO.read(getClass().getResource("/icons/app-icon.png")));
        } catch (Exception e) {
            logger.warn("Could not load application icon");
        }
    }

    private void createLayout() {
        setLayout(new BorderLayout(0, 0));
        
        // Create main components
        createHeaderPanel();
        createSidebarPanel();
        createMainContentPanel();
        createStatusPanel();
        
        // Add components to frame
        add(headerPanel, BorderLayout.NORTH);
        add(sidebarPanel, BorderLayout.WEST);
        add(mainContentPanel, BorderLayout.CENTER);
        add(statusPanel, BorderLayout.SOUTH);
    }

    private void createHeaderPanel() {
        headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(CARD_BACKGROUND);
        headerPanel.setBorder(BorderFactory.createMatteBorder(0, 0, 1, 0, BORDER_COLOR));
        headerPanel.setPreferredSize(new Dimension(0, 80));
        
        // Left side - Logo and title
        JPanel leftPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 20, 0));
        leftPanel.setOpaque(false);
        
        // App logo
        JLabel logoLabel = new JLabel("🎬");
        logoLabel.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 32));
        logoLabel.setBorder(new EmptyBorder(24, 0, 24, 0));
        
        // App title
        JLabel titleLabel = new JLabel("TikTub Studio");
        titleLabel.setFont(TITLE_FONT);
        titleLabel.setForeground(TEXT_PRIMARY);
        titleLabel.setBorder(new EmptyBorder(30, 0, 30, 0));
        
        leftPanel.add(logoLabel);
        leftPanel.add(titleLabel);
        
        // Right side - User info and settings
        JPanel rightPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 20, 0));
        rightPanel.setOpaque(false);
        
        // AI Status indicator
        JPanel aiStatusPanel = createAIStatusIndicator();
        
        // Settings button
        ModernButton settingsButton = new ModernButton("Settings", ModernButton.ButtonStyle.GHOST);
        settingsButton.setIcon("⚙️");
        settingsButton.addActionListener(e -> showSettingsDialog());
        
        rightPanel.add(aiStatusPanel);
        rightPanel.add(settingsButton);
        
        headerPanel.add(leftPanel, BorderLayout.WEST);
        headerPanel.add(rightPanel, BorderLayout.EAST);
    }

    private JPanel createAIStatusIndicator() {
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.CENTER, 8, 0));
        panel.setOpaque(false);
        panel.setBorder(new EmptyBorder(25, 0, 25, 0));
        
        // AI status dot
        JLabel statusDot = new JLabel("●");
        statusDot.setForeground(PRIMARY_GREEN);
        statusDot.setFont(new Font("Arial", Font.PLAIN, 12));
        
        // AI status text
        JLabel statusText = new JLabel("AI Ready");
        statusText.setFont(CAPTION_FONT);
        statusText.setForeground(TEXT_SECONDARY);
        
        panel.add(statusDot);
        panel.add(statusText);
        
        return panel;
    }

    private void createSidebarPanel() {
        sidebarPanel = new JPanel();
        sidebarPanel.setLayout(new BoxLayout(sidebarPanel, BoxLayout.Y_AXIS));
        sidebarPanel.setBackground(CARD_BACKGROUND);
        sidebarPanel.setBorder(BorderFactory.createMatteBorder(0, 0, 0, 1, BORDER_COLOR));
        sidebarPanel.setPreferredSize(new Dimension(280, 0));
        
        // Add spacing at top
        sidebarPanel.add(Box.createVerticalStrut(30));
        
        // Navigation items
        addNavigationItem("📤", "Upload Video", true);
        addNavigationItem("⚙️", "Processing Options", false);
        addNavigationItem("📊", "Analysis & Preview", false);
        addNavigationItem("🎬", "Generated Videos", false);
        addNavigationItem("📁", "Export & Share", false);
        
        // Add spacing
        sidebarPanel.add(Box.createVerticalStrut(40));
        
        // Add help section
        createHelpSection();
        
        // Push everything to top
        sidebarPanel.add(Box.createVerticalGlue());
    }

    private void addNavigationItem(String icon, String text, boolean active) {
        JPanel itemPanel = new JPanel(new BorderLayout());
        itemPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 50));
        itemPanel.setPreferredSize(new Dimension(0, 50));
        itemPanel.setBorder(new EmptyBorder(8, 20, 8, 20));
        
        if (active) {
            itemPanel.setBackground(new Color(PRIMARY_GREEN.getRed(), PRIMARY_GREEN.getGreen(), PRIMARY_GREEN.getBlue(), 20));
            itemPanel.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(0, 3, 0, 0, PRIMARY_GREEN),
                new EmptyBorder(8, 17, 8, 20)
            ));
        } else {
            itemPanel.setOpaque(false);
        }
        
        // Icon
        JLabel iconLabel = new JLabel(icon);
        iconLabel.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 18));
        iconLabel.setPreferredSize(new Dimension(30, 30));
        
        // Text
        JLabel textLabel = new JLabel(text);
        textLabel.setFont(BODY_FONT);
        textLabel.setForeground(active ? PRIMARY_GREEN : TEXT_SECONDARY);
        
        itemPanel.add(iconLabel, BorderLayout.WEST);
        itemPanel.add(textLabel, BorderLayout.CENTER);
        
        // Add hover effect
        itemPanel.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                if (!active) {
                    itemPanel.setBackground(new Color(0, 0, 0, 10));
                    itemPanel.setOpaque(true);
                }
            }
            
            @Override
            public void mouseExited(MouseEvent e) {
                if (!active) {
                    itemPanel.setOpaque(false);
                }
            }
        });
        
        sidebarPanel.add(itemPanel);
    }

    private void createHelpSection() {
        JPanel helpPanel = new RoundedPanel(12);
        helpPanel.setBackground(new Color(SECONDARY_BLUE.getRed(), SECONDARY_BLUE.getGreen(), SECONDARY_BLUE.getBlue(), 20));
        helpPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        helpPanel.setLayout(new BoxLayout(helpPanel, BoxLayout.Y_AXIS));
        helpPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 150));
        
        // Help icon and title
        JLabel helpIcon = new JLabel("💡");
        helpIcon.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 24));
        helpIcon.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel helpTitle = new JLabel("Need Help?");
        helpTitle.setFont(new Font("Segoe UI", Font.BOLD, 14));
        helpTitle.setForeground(TEXT_PRIMARY);
        helpTitle.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel helpText = new JLabel("<html><center>Check our tutorial for<br>creating amazing short videos</center></html>");
        helpText.setFont(CAPTION_FONT);
        helpText.setForeground(TEXT_SECONDARY);
        helpText.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Help button
        ModernButton helpButton = new ModernButton("View Tutorial", ModernButton.ButtonStyle.OUTLINE);
        helpButton.setAlignmentX(Component.CENTER_ALIGNMENT);
        helpButton.addActionListener(e -> openTutorial());
        
        helpPanel.add(helpIcon);
        helpPanel.add(Box.createVerticalStrut(8));
        helpPanel.add(helpTitle);
        helpPanel.add(Box.createVerticalStrut(4));
        helpPanel.add(helpText);
        helpPanel.add(Box.createVerticalStrut(12));
        helpPanel.add(helpButton);
        
        // Wrap in container with margins
        JPanel helpContainer = new JPanel(new BorderLayout());
        helpContainer.setOpaque(false);
        helpContainer.setBorder(new EmptyBorder(0, 20, 20, 20));
        helpContainer.add(helpPanel, BorderLayout.CENTER);
        
        sidebarPanel.add(helpContainer);
    }

    private void createMainContentPanel() {
        mainContentPanel = new JPanel(new BorderLayout());
        mainContentPanel.setBackground(BACKGROUND_LIGHT);
        mainContentPanel.setBorder(new EmptyBorder(30, 30, 30, 30));
        
        // Create cards
        createContentCards();
        
        // Initial view - show upload card
        showUploadView();
    }

    private void createContentCards() {
        // Upload Card
        uploadCard = new VideoUploadCard();
        uploadCard.setFileSelectedCallback(this::onVideoFileSelected);
        
        // Processing Options Card
        optionsCard = new ProcessingOptionsCard();
        
        // Progress Card
        progressCard = new ProgressCard();
        
        // Results Card
        resultsCard = new ResultsCard();
    }

    private void showUploadView() {
        mainContentPanel.removeAll();
        
        // Welcome message
        JPanel welcomePanel = createWelcomePanel();
        
        mainContentPanel.add(welcomePanel, BorderLayout.NORTH);
        mainContentPanel.add(uploadCard, BorderLayout.CENTER);
        
        revalidate();
        repaint();
    }

    private JPanel createWelcomePanel() {
        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.setOpaque(false);
        panel.setBorder(new EmptyBorder(0, 0, 30, 0));
        
        // Main title
        JLabel titleLabel = new JLabel("Transform Your Long Videos into Viral Shorts");
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 32));
        titleLabel.setForeground(TEXT_PRIMARY);
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Subtitle
        JLabel subtitleLabel = new JLabel("AI-powered video analysis finds the best moments and adds professional effects automatically");
        subtitleLabel.setFont(SUBTITLE_FONT);
        subtitleLabel.setForeground(TEXT_SECONDARY);
        subtitleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Features list
        JPanel featuresPanel = createFeaturesPanel();
        
        panel.add(titleLabel);
        panel.add(Box.createVerticalStrut(12));
        panel.add(subtitleLabel);
        panel.add(Box.createVerticalStrut(30));
        panel.add(featuresPanel);
        
        return panel;
    }

    private JPanel createFeaturesPanel() {
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.CENTER, 40, 0));
        panel.setOpaque(false);
        
        String[] features = {
            "🤖|AI Scene Detection|Automatically finds the most engaging moments",
            "🎨|Smart Effects|Applies perfect effects based on content analysis", 
            "📝|Auto Subtitles|Generates accurate subtitles with animations",
            "📱|Mobile Ready|Optimized for TikTok, YouTube Shorts & Reels"
        };
        
        for (String feature : features) {
            String[] parts = feature.split("\\|");
            panel.add(createFeatureCard(parts[0], parts[1], parts[2]));
        }
        
        return panel;
    }

    private JPanel createFeatureCard(String icon, String title, String description) {
        JPanel card = new RoundedPanel(12);
        card.setBackground(CARD_BACKGROUND);
        card.setBorder(new EmptyBorder(20, 20, 20, 20));
        card.setPreferredSize(new Dimension(200, 120));
        card.setLayout(new BoxLayout(card, BoxLayout.Y_AXIS));
        
        // Add subtle shadow effect
        card.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createMatteBorder(0, 0, 2, 2, new Color(0, 0, 0, 10)),
            new EmptyBorder(20, 20, 18, 18)
        ));
        
        JLabel iconLabel = new JLabel(icon);
        iconLabel.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 28));
        iconLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel titleLabel = new JLabel(title);
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 14));
        titleLabel.setForeground(TEXT_PRIMARY);
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel descLabel = new JLabel("<html><center>" + description + "</center></html>");
        descLabel.setFont(CAPTION_FONT);
        descLabel.setForeground(TEXT_SECONDARY);
        descLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        card.add(iconLabel);
        card.add(Box.createVerticalStrut(8));
        card.add(titleLabel);
        card.add(Box.createVerticalStrut(4));
        card.add(descLabel);
        
        return card;
    }

    private void createStatusPanel() {
        statusPanel = new JPanel(new BorderLayout());
        statusPanel.setBackground(CARD_BACKGROUND);
        statusPanel.setBorder(BorderFactory.createMatteBorder(1, 0, 0, 0, BORDER_COLOR));
        statusPanel.setPreferredSize(new Dimension(0, 60));
        
        // Left side - Status text
        statusLabel = new JLabel("Ready to create amazing short videos");
        statusLabel.setFont(BODY_FONT);
        statusLabel.setForeground(TEXT_SECONDARY);
        statusLabel.setBorder(new EmptyBorder(0, 20, 0, 0));
        
        // Right side - Progress and action button
        JPanel rightPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 20, 0));
        rightPanel.setOpaque(false);
        
        // Global progress bar (initially hidden)
        globalProgressBar = new JProgressBar(0, 100);
        globalProgressBar.setStringPainted(true);
        globalProgressBar.setPreferredSize(new Dimension(200, 25));
        globalProgressBar.setVisible(false);
        
        // Main process button
        processButton = new ModernButton("Select Video to Start", ModernButton.ButtonStyle.PRIMARY);
        processButton.setIcon("🚀");
        processButton.setEnabled(false);
        processButton.addActionListener(this::onProcessButtonClicked);
        
        rightPanel.add(globalProgressBar);
        rightPanel.add(processButton);
        
        statusPanel.add(statusLabel, BorderLayout.WEST);
        statusPanel.add(rightPanel, BorderLayout.EAST);
    }

    private void setupEventHandlers() {
        // Window close handler
        addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                onApplicationClosing();
            }
        });
    }

    private void showWelcomeAnimation() {
        // Simple fade-in animation
        setOpacity(0.0f);
        setVisible(true);
        
        Timer fadeTimer = new Timer(50, null);
        fadeTimer.addActionListener(new ActionListener() {
            float opacity = 0.0f;
            
            @Override
            public void actionPerformed(ActionEvent e) {
                opacity += 0.1f;
                if (opacity >= 1.0f) {
                    opacity = 1.0f;
                    fadeTimer.stop();
                }
                setOpacity(opacity);
            }
        });
        fadeTimer.start();
    }

    // Event Handlers
    private void onVideoFileSelected(File file) {
        this.selectedVideoFile = file;
        
        // Update UI
        statusLabel.setText("Video selected: " + file.getName());
        processButton.setText("Analyze & Process Video");
        processButton.setEnabled(true);
        
        // Update upload card to show selected file
        uploadCard.showSelectedFile(file);
        
        // Auto-advance to options if this is the first time
        showProcessingOptionsAnimation();
        
        logger.info("Video file selected: {}", file.getAbsolutePath());
    }

    private void showProcessingOptionsAnimation() {
        // Smooth transition to show processing options
        Timer slideTimer = new Timer(30, null);
        final int[] slidePosition = {mainContentPanel.getHeight()};
        
        // Add options card below current view
        mainContentPanel.add(optionsCard, BorderLayout.SOUTH);
        optionsCard.setLocation(0, slidePosition[0]);
        
        slideTimer.addActionListener(e -> {
            slidePosition[0] -= 20;
            if (slidePosition[0] <= 0) {
                slidePosition[0] = 0;
                slideTimer.stop();
            }
            optionsCard.setLocation(0, slidePosition[0]);
            revalidate();
            repaint();
        });
        
        slideTimer.start();
    }

    private void onProcessButtonClicked(ActionEvent e) {
        if (!isProcessing) {
            startVideoProcessing();
        } else {
            cancelVideoProcessing();
        }
    }

    private void startVideoProcessing() {
        if (selectedVideoFile == null) {
            showErrorDialog("Please select a video file first");
            return;
        }
        
        // Get processing options
        Map<String, Object> processingOptions = optionsCard.getProcessingOptions();
        
        // Update UI for processing state
        isProcessing = true;
        processButton.setText("Cancel Processing");
        processButton.setButtonStyle(ModernButton.ButtonStyle.DANGER);
        globalProgressBar.setVisible(true);
        
        // Show progress view
        showProgressView();
        
        // Start processing in background
        CompletableFuture.runAsync(() -> {
            try {
                processVideoAsync(selectedVideoFile, processingOptions);
            } catch (Exception ex) {
                SwingUtilities.invokeLater(() -> {
                    handleProcessingError(ex);
                });
            }
        });
        
        logger.info("Started video processing for: {}", selectedVideoFile.getName());
    }

    private void processVideoAsync(File videoFile, Map<String, Object> options) {
        try {
            // Update progress: Uploading
            updateProgress(10, "Uploading video...");
            String videoId = apiClient.uploadVideo(videoFile);
            
            // Update progress: Analyzing
            updateProgress(25, "AI analyzing video content...");
            JsonObject analysisResult = apiClient.analyzeVideo(videoId);
            
            // Update progress: Generating subtitles
            updateProgress(50, "Generating AI subtitles...");
            JsonObject subtitleResult = apiClient.generateSubtitles(videoId);
            
            // Update progress: Applying effects
            updateProgress(75, "Applying smart effects and transitions...");
            JsonObject effectsResult = apiClient.generateEffects(videoId, options);
            
            // Update progress: Processing final video
            updateProgress(90, "Creating final short videos...");
            JsonObject processingResult = apiClient.processVideo(videoId, options);
            
            // Update progress: Complete
            updateProgress(100, "Processing complete!");
            
            // Show results
            SwingUtilities.invokeLater(() -> {
                showProcessingResults(processingResult);
            });
            
        } catch (Exception e) {
            logger.error("Error during video processing", e);
            SwingUtilities.invokeLater(() -> {
                handleProcessingError(e);
            });
        }
    }

    private void updateProgress(int percentage, String message) {
        SwingUtilities.invokeLater(() -> {
            globalProgressBar.setValue(percentage);
            globalProgressBar.setString(percentage + "%");
            statusLabel.setText(message);
            progressCard.updateProgress(percentage, message);
        });
    }

    private void showProgressView() {
        mainContentPanel.removeAll();
        mainContentPanel.add(progressCard, BorderLayout.CENTER);
        revalidate();
        repaint();
    }

    private void showProcessingResults(JsonObject results) {
        // Reset processing state
        isProcessing = false;
        processButton.setText("Process Another Video");
        processButton.setButtonStyle(ModernButton.ButtonStyle.PRIMARY);
        globalProgressBar.setVisible(false);
        
        // Update results card with data
        resultsCard.setResults(results);
        
        // Show results view
        mainContentPanel.removeAll();
        mainContentPanel.add(resultsCard, BorderLayout.CENTER);
        revalidate();
        repaint();
        
        // Show success notification
        showSuccessNotification("Video processing completed successfully!");
        
        logger.info("Video processing completed successfully");
    }

    private void handleProcessingError(Exception error) {
        // Reset processing state
        isProcessing = false;
        processButton.setText("Try Again");
        processButton.setButtonStyle(ModernButton.ButtonStyle.PRIMARY);
        globalProgressBar.setVisible(false);
        
        // Update status
        statusLabel.setText("Processing failed: " + error.getMessage());
        
        // Show error dialog
        showErrorDialog("Processing failed: " + error.getMessage());
        
        logger.error("Video processing failed", error);
    }

    private void cancelVideoProcessing() {
        // Cancel the processing
        apiClient.cancelProcessing();
        
        // Reset UI state
        isProcessing = false;
        processButton.setText("Process Video");
        processButton.setButtonStyle(ModernButton.ButtonStyle.PRIMARY);
        globalProgressBar.setVisible(false);
        statusLabel.setText("Processing cancelled");
        
        // Return to upload view
        showUploadView();
        
        logger.info("Video processing cancelled by user");
    }

    // Utility Methods
    private void showSettingsDialog() {
        SettingsDialog dialog = new SettingsDialog(this);
        dialog.setVisible(true);
    }

    private void openTutorial() {
        try {
            Desktop.getDesktop().browse(new java.net.URI("https://tiktubstudio.com/tutorial"));
        } catch (Exception e) {
            logger.warn("Could not open tutorial URL", e);
            showInfoDialog("Tutorial", "Visit https://tiktubstudio.com/tutorial for help");
        }
    }

    private void showErrorDialog(String message) {
        NotificationDialog.showError(this, "Error", message);
    }

    private void showInfoDialog(String title, String message) {
        NotificationDialog.showInfo(this, title, message);
    }

    private void showSuccessNotification(String message) {
        NotificationDialog.showSuccess(this, "Success", message);
    }

    private void onApplicationClosing() {
        if (isProcessing) {
            int option = JOptionPane.showConfirmDialog(
                this,
                "Video processing is still running. Do you want to cancel and exit?",
                "Confirm Exit",
                JOptionPane.YES_NO_OPTION,
                JOptionPane.WARNING_MESSAGE
            );
            
            if (option == JOptionPane.YES_OPTION) {
                cancelVideoProcessing();
                System.exit(0);
            }
        } else {
            System.exit(0);
        }
    }

    // Main method for testing
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(new com.formdev.flatlaf.FlatDarkLaf());
                new MainWindow().setVisible(true);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }
}