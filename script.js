const form = document.querySelector('#career-form');
const skills = document.querySelector('#skills');
const hours = document.querySelector('#hours');
const errorBox = document.querySelector('#error');

let latest = null;
let completedWeeks = new Set();

// Study hours display
hours.addEventListener('input', () => {
    document.querySelector('#hours-value').value =
        `${hours.value} hour${hours.value === '1' ? '' : 's'}`;
});

// Add skill buttons
document.querySelectorAll('[data-skill]').forEach(button => {
    button.addEventListener('click', () => {
        const value = button.dataset.skill;
        const list = skills.value.split(',')
            .map(x => x.trim())
            .filter(Boolean);

        if (!list.some(x => x.toLowerCase() === value.toLowerCase())) {
            list.push(value);
        }

        skills.value = list.join(', ');
        skills.focus();
    });
});

// Create skill tags
function tag(text, missing = false) {
    const el = document.createElement('span');
    el.className = 'tag' + (missing ? ' missing' : '');
    el.textContent = text;
    return el;
}

// Progress tracker
function updateProgress(total) {
    const completed = completedWeeks.size;
    const percentage = Math.round((completed / total) * 100);

    document.querySelector('#progress-text').textContent =
        `${completed} of ${total} weeks completed (${percentage}%)`;

    document.querySelector('#progress-fill').style.width =
        `${percentage}%`;
}

function addProgressCheckboxes(data) {
    completedWeeks.clear();

    document.querySelectorAll('.week').forEach((card, index) => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';

        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                completedWeeks.add(index);
            } else {
                completedWeeks.delete(index);
            }

            updateProgress(data.roadmap.length);
        });

        card.prepend(checkbox);
    });

    updateProgress(data.roadmap.length);
}

// Display generated roadmap
function render(data) {
    latest = data;

    document.querySelector('#empty').classList.add('hide');
    document.querySelector('#results').classList.remove('hide');
    document.querySelector('#status').textContent = 'Roadmap ready';

    document.querySelector('#score').textContent =
        data.skill_match_percentage + '%';

    document.querySelector('#ring-value').textContent =
        data.skill_match_percentage + '%';

    document.querySelector('#ring').style.background =
        `conic-gradient(var(--purple) ${data.skill_match_percentage * 3.6}deg, #e3e5f1 0deg)`;

    document.querySelector('#summary').textContent =
        `${data.target_role} · ${data.experience} · ${data.education}`;

    document.querySelector('#matched-count').textContent =
        data.skills_matched.length;

    document.querySelector('#gap-count').textContent =
        data.skill_gaps.length;

    const matched = document.querySelector('#matched');

    matched.replaceChildren(
        ...(data.skills_matched.length
            ? data.skills_matched.map(x => tag(x))
            : [tag('No matching skills listed yet')])
    );

    const gaps = document.querySelector('#gaps');

    gaps.replaceChildren(
        ...(data.skill_gaps.length
            ? data.skill_gaps.map(x => tag(x, true))
            : [tag('No gaps in this checklist')])
    );

    const weeks = document.querySelector('#weeks');
    weeks.replaceChildren();

    data.roadmap.forEach(item => {
        const card = document.createElement('article');
        card.className = 'week';

        const title = document.createElement('strong');
        title.textContent = `WEEK ${item.week} · ${item.title}`;

        const focus = document.createElement('p');
        focus.textContent = item.focus;

        const task = document.createElement('p');
        task.className = 'task';
        task.textContent = 'Practice task: ' + item.task;

        const time = document.createElement('p');
        time.textContent =
            `Suggested study time: ${item.estimated_hours} hours`;

        card.append(title, focus, task, time);
        weeks.append(card);
    });

    // Add progress checkboxes
    addProgressCheckboxes(data);

    // Display recommendations
    const list = document.querySelector('#recommendations');
    list.replaceChildren();

    data.recommendations.forEach(text => {
        const li = document.createElement('li');
        li.textContent = text;
        list.append(li);
    });

    document.querySelector('#note').textContent = data.note;

    // Display AI-generated career guidance
    let aiSection = document.querySelector('#ai-guidance');

    if (!aiSection) {
        aiSection = document.createElement('section');
        aiSection.id = 'ai-guidance';
        aiSection.className = 'ai-guidance';

        const noteSection = document.querySelector('#note');
        noteSection.parentNode.insertBefore(aiSection, noteSection);
    }

    aiSection.replaceChildren();

    const aiTitle = document.createElement('h2');
    aiTitle.textContent = 'AI Career Guidance';

    const aiContent = document.createElement('p');
    const guidance = data.ai_guidance ||
    'AI guidance is not available right now.';

const cleanGuidance = guidance.replace(/\\(?=\s|[.+])/g, '');
aiContent.innerHTML = cleanGuidance
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/^### (.*)$/gm, '<h3>$1</h3>')
    .replace(/^## (.*)$/gm, '<h2>$1</h2>')
    .replace(/^# (.*)$/gm, '<h2>$1</h2>')
    .replace(/^\s*[-*] (.*)$/gm, '• $1')
    .replace(/\n/g, '<br>');
    aiSection.append(aiTitle, aiContent);
}

// Generate roadmap form submission
form.addEventListener('submit', async e => {
    e.preventDefault();

    errorBox.textContent = '';

    const button = document.querySelector('#submit');
    button.disabled = true;
    button.textContent = 'Building roadmap…';

    try {
        const response = await fetch('/api/roadmap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                education: document.querySelector('#education').value.trim(),
                target_role: document.querySelector('#role').value,
                experience: document.querySelector('#experience').value,
                skills: skills.value,
                hours_per_week: Number(hours.value)
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not generate roadmap');
        }

        render(data);

        document.querySelector('#results').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

    } catch (err) {
        errorBox.textContent =
            err.message + ' Check that the Flask server is running.';
    } finally {
        button.disabled = false;
        button.innerHTML = 'Generate my roadmap <span>→</span>';
    }
});

// Download roadmap as PDF
document.querySelector('#download').addEventListener('click', () => {
    if (!latest) return;

    if (!window.jspdf) {
        alert('PDF library not loaded. Please check your internet connection.');
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    let y = 20;

    doc.setFontSize(18);
    doc.text('PATHPILOT - CAREER ROADMAP', 20, y);
    y += 15;

    doc.setFontSize(12);

    const addText = (text) => {
        const lines = doc.splitTextToSize(String(text), 170);

        if (y + lines.length * 7 > 280) {
            doc.addPage();
            y = 20;
        }

        doc.text(lines, 20, y);
        y += lines.length * 7;
    };

    addText(`Target Role: ${latest.target_role}`);
    addText(`Education: ${latest.education}`);
    addText(`Experience: ${latest.experience}`);
    addText(`Skill Match: ${latest.skill_match_percentage}%`);
    addText(`Skills Matched: ${latest.skills_matched.join(', ') || 'None'}`);
    addText(`Skills To Learn: ${latest.skill_gaps.join(', ') || 'None'}`);

    y += 5;
    addText('SIX-WEEK LEARNING PLAN');

    latest.roadmap.forEach(week => {
        y += 4;
        addText(`Week ${week.week}: ${week.title}`);
        addText(week.focus);
        addText(`Practice Task: ${week.task}`);
        addText(`Study Hours: ${week.estimated_hours}`);
    });

    y += 5;
    addText('RECOMMENDATIONS');

    latest.recommendations.forEach(item => {
        addText('- ' + item);
    });

    addText(latest.note);

    // Include AI guidance in downloaded PDF
    if (latest.ai_guidance) {
        y += 5;
        addText('AI CAREER GUIDANCE');
        addText(latest.ai_guidance);
    }

    doc.save('PathPilot-Career-Roadmap.pdf');
});
