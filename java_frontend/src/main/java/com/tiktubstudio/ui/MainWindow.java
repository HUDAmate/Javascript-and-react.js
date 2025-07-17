package com.tiktubstudio.ui;

import com.tiktubstudio.api.ApiClient;
import com.tiktubstudio.ui.components.*;
import com.tiktubstudio.ui.panels.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;

/**
 * Main window untuk TikTub Studio application
 */
public class MainWindow extends JFrame {
    private static final Logger logger = LoggerFactory.getLogger(MainWindow.class);
    
    // Components
    private JTabbedPane tabbedPane;
    private UploadPanel uploadPanel;
    private ProcessingPanel processingPanel;
    private ResultsPanel resultsPanel;
    private SettingsPanel settingsPanel;
    private StatusBar statusBar;
    
    // API Client
    private ApiClient apiClient;
    
    public MainWindow() {
        initializeComponents();
        setupUI();
        setupEventHandlers();
        
        logger.info("Main window initialized");
    }
    
    private void initializeComponents() {
        // Initialize API client
        apiClient = new ApiClient("http://localhost:5000");
        
        // Initialize panels
        uploadPanel = new UploadPanel(apiClient, this);
        processingPanel = new ProcessingPanel(apiClient, this);
        resultsPanel = new ResultsPanel(apiClient, this);
        settingsPanel = new SettingsPanel(this);
        
        // Initialize status bar
        statusBar = new StatusBar();
    }
    
    private void setupUI() {
        setTitle("TikTub Studio - AI-Powered Short Video Creator");
        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        
        // Set icon
        try {
            // You can add custom icon here
            setIconImage(createIcon());
        } catch (Exception e) {
            logger.warn("Could not set application icon", e);
        }
        
        // Set size dan position
        setSize(1200, 800);
        setMinimumSize(new Dimension(1000, 600));
        setLocationRelativeTo(null);
        
        // Create main layout
        setLayout(new BorderLayout());
        
        // Create header
        JPanel header = createHeader();
        add(header, BorderLayout.NORTH);
        
        // Create tabbed pane
        tabbedPane = new JTabbedPane(JTabbedPane.TOP);
        tabbedPane.setTabLayoutPolicy(JTabbedPane.SCROLL_TAB_LAYOUT);
        
        // Add tabs
        tabbedPane.addTab("📁 Upload Video", uploadPanel);
        tabbedPane.addTab("⚙️ Processing", processingPanel);
        tabbedPane.addTab("🎬 Results", resultsPanel);
        tabbedPane.addTab("⚙️ Settings", settingsPanel);
        
        // Style tabs
        styleTabPane();
        
        add(tabbedPane, BorderLayout.CENTER);
        
        // Add status bar
        add(statusBar, BorderLayout.SOUTH);
        
        // Initially disable processing and results tabs
        tabbedPane.setEnabledAt(1, false);
        tabbedPane.setEnabledAt(2, false);
    }
    
    private JPanel createHeader() {
        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(new Color(20, 20, 23));
        header.setBorder(new EmptyBorder(15, 20, 15, 20));
        
        // Logo and title
        JPanel titlePanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        titlePanel.setBackground(new Color(20, 20, 23));
        
        JLabel logoLabel = new JLabel("🎬");
        logoLabel.setFont(new Font("Arial", Font.PLAIN, 24));
        
        JLabel titleLabel = new JLabel("TikTub Studio");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        titleLabel.setForeground(Color.WHITE);
        
        JLabel subtitleLabel = new JLabel("Transform long videos into engaging short clips");
        subtitleLabel.setFont(new Font("Arial", Font.PLAIN, 12));
        subtitleLabel.setForeground(new Color(180, 180, 180));
        
        titlePanel.add(logoLabel);
        titlePanel.add(Box.createHorizontalStrut(10));
        titlePanel.add(titleLabel);
        titlePanel.add(Box.createHorizontalStrut(10));
        titlePanel.add(subtitleLabel);
        
        // Action buttons
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        buttonPanel.setBackground(new Color(20, 20, 23));
        
        JButton helpButton = new JButton("❓ Help");
        JButton aboutButton = new JButton("ℹ️ About");
        
        styleHeaderButton(helpButton);
        styleHeaderButton(aboutButton);
        
        helpButton.addActionListener(e -> showHelpDialog());
        aboutButton.addActionListener(e -> showAboutDialog());
        
        buttonPanel.add(helpButton);
        buttonPanel.add(Box.createHorizontalStrut(5));
        buttonPanel.add(aboutButton);
        
        header.add(titlePanel, BorderLayout.WEST);
        header.add(buttonPanel, BorderLayout.EAST);
        
        return header;
    }
    
    private void styleHeaderButton(JButton button) {
        button.setBackground(new Color(45, 45, 48));
        button.setForeground(Color.WHITE);
        button.setBorder(BorderFactory.createEmptyBorder(8, 16, 8, 16));
        button.setFocusPainted(false);
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        
        // Hover effect
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(60, 60, 65));
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(45, 45, 48));
            }
        });
    }
    
    private void styleTabPane() {
        tabbedPane.setBackground(new Color(32, 32, 35));
        tabbedPane.setForeground(Color.WHITE);
        
        // Custom tab styling
        for (int i = 0; i < tabbedPane.getTabCount(); i++) {
            Component tab = tabbedPane.getTabComponentAt(i);
            if (tab == null) {
                // Create custom tab component if needed
            }
        }
    }
    
    private Image createIcon() {
        // Create simple icon
        BufferedImage icon = new BufferedImage(32, 32, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2d = icon.createGraphics();
        
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        // Background circle
        g2d.setColor(new Color(255, 0, 80));
        g2d.fillOval(2, 2, 28, 28);
        
        // Play button
        g2d.setColor(Color.WHITE);
        int[] xPoints = {12, 12, 22};
        int[] yPoints = {10, 22, 16};
        g2d.fillPolygon(xPoints, yPoints, 3);
        
        g2d.dispose();
        return icon;
    }
    
    private void setupEventHandlers() {
        // Window closing handler
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                handleWindowClosing();
            }
        });
        
        // Tab change handler
        tabbedPane.addChangeListener(e -> {
            int selectedIndex = tabbedPane.getSelectedIndex();
            updateStatusBar(selectedIndex);
        });
    }
    
    private void handleWindowClosing() {
        int option = JOptionPane.showConfirmDialog(
            this,
            "Apakah Anda yakin ingin keluar dari TikTub Studio?",
            "Konfirmasi Keluar",
            JOptionPane.YES_NO_OPTION,
            JOptionPane.QUESTION_MESSAGE
        );
        
        if (option == JOptionPane.YES_OPTION) {
            // Check for ongoing processing
            if (processingPanel.isProcessing()) {
                int continueOption = JOptionPane.showConfirmDialog(
                    this,
                    "Ada proses yang sedang berjalan. Yakin ingin keluar?",
                    "Proses Sedang Berjalan",
                    JOptionPane.YES_NO_OPTION,
                    JOptionPane.WARNING_MESSAGE
                );
                
                if (continueOption != JOptionPane.YES_OPTION) {
                    return;
                }
            }
            
            logger.info("Application closing");
            System.exit(0);
        }
    }
    
    private void updateStatusBar(int tabIndex) {
        switch (tabIndex) {
            case 0:
                statusBar.setMessage("Pilih video untuk diproses");
                break;
            case 1:
                statusBar.setMessage("Konfigurasikan dan jalankan proses");
                break;
            case 2:
                statusBar.setMessage("Lihat dan download hasil video");
                break;
            case 3:
                statusBar.setMessage("Atur preferensi aplikasi");
                break;
            default:
                statusBar.setMessage("Ready");
        }
    }
    
    private void showHelpDialog() {
        JDialog helpDialog = new JDialog(this, "Help - TikTub Studio", true);
        helpDialog.setSize(600, 500);
        helpDialog.setLocationRelativeTo(this);
        
        JTextArea helpText = new JTextArea();
        helpText.setEditable(false);
        helpText.setBackground(new Color(45, 45, 48));
        helpText.setForeground(Color.WHITE);
        helpText.setFont(new Font("Arial", Font.PLAIN, 12));
        helpText.setMargin(new Insets(20, 20, 20, 20));
        
        String helpContent = """
            🎬 TikTub Studio - Panduan Penggunaan
            
            1. UPLOAD VIDEO
               • Klik tombol "Choose Video" untuk memilih video
               • Format yang didukung: MP4, MOV, AVI, MKV
               • Ukuran maksimal: 2GB
               • Durasi minimal: 2 menit
            
            2. PROCESSING
               • Pilih platform target (TikTok, YouTube Shorts, Instagram Reels)
               • Atur jumlah segmen yang diinginkan (1-10)
               • Pilih tema efek (Auto, Energetic, Calm, Educational, dll)
               • Pilih bahasa untuk subtitle
               • Klik "Start Processing" untuk memulai
            
            3. RESULTS
               • Preview video hasil processing
               • Download video yang diinginkan
               • Lihat informasi detail setiap video
            
            💡 TIPS:
               • Video dengan durasi 10-30 menit memberikan hasil terbaik
               • Pastikan video memiliki audio yang jelas untuk subtitle
               • Gunakan mode "Auto" untuk deteksi tema otomatis
               • Processing membutuhkan waktu 2-10 menit tergantung durasi video
            
            🔧 TROUBLESHOOTING:
               • Jika upload gagal, periksa koneksi internet
               • Jika processing lambat, tutup aplikasi lain
               • Jika error, restart aplikasi dan coba lagi
            """;
        
        helpText.setText(helpContent);
        
        JScrollPane scrollPane = new JScrollPane(helpText);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        
        helpDialog.add(scrollPane);
        helpDialog.setVisible(true);
    }
    
    private void showAboutDialog() {
        JDialog aboutDialog = new JDialog(this, "About - TikTub Studio", true);
        aboutDialog.setSize(400, 300);
        aboutDialog.setLocationRelativeTo(this);
        aboutDialog.setLayout(new BorderLayout());
        
        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.setBackground(new Color(32, 32, 35));
        panel.setBorder(new EmptyBorder(30, 30, 30, 30));
        
        JLabel iconLabel = new JLabel("🎬", JLabel.CENTER);
        iconLabel.setFont(new Font("Arial", Font.PLAIN, 48));
        iconLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel titleLabel = new JLabel("TikTub Studio", JLabel.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel versionLabel = new JLabel("Version 1.0.0", JLabel.CENTER);
        versionLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        versionLabel.setForeground(new Color(180, 180, 180));
        versionLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel descLabel = new JLabel("<html><center>AI-Powered Short Video Creator<br>Transform long videos into engaging clips</center></html>", JLabel.CENTER);
        descLabel.setFont(new Font("Arial", Font.PLAIN, 12));
        descLabel.setForeground(new Color(160, 160, 160));
        descLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel copyrightLabel = new JLabel("© 2024 TikTub Studio", JLabel.CENTER);
        copyrightLabel.setFont(new Font("Arial", Font.PLAIN, 10));
        copyrightLabel.setForeground(new Color(120, 120, 120));
        copyrightLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        panel.add(iconLabel);
        panel.add(Box.createVerticalStrut(10));
        panel.add(titleLabel);
        panel.add(Box.createVerticalStrut(5));
        panel.add(versionLabel);
        panel.add(Box.createVerticalStrut(15));
        panel.add(descLabel);
        panel.add(Box.createVerticalGlue());
        panel.add(copyrightLabel);
        
        aboutDialog.add(panel, BorderLayout.CENTER);
        aboutDialog.setVisible(true);
    }
    
    // Public methods untuk inter-panel communication
    public void switchToProcessingTab() {
        tabbedPane.setEnabledAt(1, true);
        tabbedPane.setSelectedIndex(1);
    }
    
    public void switchToResultsTab() {
        tabbedPane.setEnabledAt(2, true);
        tabbedPane.setSelectedIndex(2);
    }
    
    public void updateStatus(String message) {
        statusBar.setMessage(message);
    }
    
    public void showProgress(String message, int progress) {
        statusBar.setProgress(message, progress);
    }
    
    public void hideProgress() {
        statusBar.hideProgress();
    }
    
    public UploadPanel getUploadPanel() {
        return uploadPanel;
    }
    
    public ProcessingPanel getProcessingPanel() {
        return processingPanel;
    }
    
    public ResultsPanel getResultsPanel() {
        return resultsPanel;
    }
}