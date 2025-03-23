import React, { useState } from 'react';
import { motion } from 'framer-motion';
import styles from '../styles/WelcomePage.module.css';

export default function WelcomePage() {
    const [linkedinUrl, setLinkedinUrl] = useState('');
    const [userAdded, setUserAdded] = useState(false);

    const isValidLinkedInUrl = (url) => {
        const linkedInRegex = /^(https?:\/\/)?(www\.)?linkedin\.com\/.*$/;
        return linkedInRegex.test(url);
    };

    const handleAddUser = () => {
        if (linkedinUrl.trim() === '') {
            alert('Please enter a valid LinkedIn URL');
            return;
        }

        if (!isValidLinkedInUrl(linkedinUrl)) {
            alert('Invalid LinkedIn URL. Please enter a valid LinkedIn profile URL.');
            return;
        }

        setUserAdded(true);
        alert('User added successfully!');
    };

    const handleGoHome = () => {
        window.location.href = '/home';
    };

    return (
        <div className={styles.container}>
            <motion.div
                className={styles.card}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
            >
                <h1 className={styles.title}>Welcome to InfluenceIQ</h1>
                <p className={styles.description}>Empower your influence with smart insights!</p>

                {userAdded ? (
                    <div>
                        <p className={styles.success}>User added successfully! 🎉</p>
                        <button className={styles.button} onClick={handleGoHome}>Go to Home</button>
                    </div>
                ) : (
                    <div>
                        <input
                            type="url"
                            className={styles.input}
                            placeholder="Enter your LinkedIn URL"
                            value={linkedinUrl}
                            onChange={(e) => setLinkedinUrl(e.target.value)}
                        />
                        <button className={styles.button} onClick={handleAddUser}>Add User</button>
                    </div>
                )}
            </motion.div>
        </div>
    );
}
