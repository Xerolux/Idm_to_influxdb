/* Xerolux 2026 */
/**
 * Query Parser for Variable Substitution
 *
 * Replaces template variables in queries with actual values.
 * Supports multiple syntaxes:
 * - ${variable}
 * - $variable
 * - {variable} (Grafana style)
 */

/**
 * Substitute variables in a query string
 * @param {string} query - The query with variable placeholders
 * @param {Object} variables - Object with variable values (e.g., {circuit: 'A'})
 * @returns {string} - The query with substituted values
 */
export function substituteVariables(query, variables = {}) {
    if (!query || typeof query !== 'string') {
        return query;
    }

    let result = query;

    // Replace ${var} syntax first
    result = result.replace(/\$\{([^}]+)\}/g, (match, varName) => {
        if (varName in variables && variables[varName] !== null && variables[varName] !== undefined) {
            return String(variables[varName]);
        }
        return match;
    });

    // Then replace $var syntax (word boundary to avoid partial replacements)
    result = result.replace(/\$([a-zA-Z_][a-zA-Z0-9_]*)/g, (match, varName) => {
        if (varName in variables && variables[varName] !== null && variables[varName] !== undefined) {
            return String(variables[varName]);
        }
        return match;
    });

    // Replace {var} syntax (Grafana style)
    result = result.replace(/\{([a-zA-Z_][a-zA-Z0-9_]*)\}/g, (match, varName) => {
        if (varName in variables && variables[varName] !== null && variables[varName] !== undefined) {
            return String(variables[varName]);
        }
        return match;
    });

    return result;
}

/**
 * Extract variable names from a query string
 * @param {string} query - The query to parse
 * @returns {Array<string>} - Array of variable names
 */
export function extractVariables(query) {
    if (!query || typeof query !== 'string') {
        return [];
    }

    const variables = new Set();

    // Extract ${var} syntax
    const bracedMatches = query.matchAll(/\$\{([^}]+)\}/g);
    for (const match of bracedMatches) {
        variables.add(match[1]);
    }

    // Extract $var syntax
    const simpleMatches = query.matchAll(/\$([a-zA-Z_][a-zA-Z0-9_]*)/g);
    for (const match of simpleMatches) {
        variables.add(match[1]);
    }

    // Extract {var} syntax
    const grafanaMatches = query.matchAll(/\{([a-zA-Z_][a-zA-Z0-9_]*)\}/g);
    for (const match of grafanaMatches) {
        variables.add(match[1]);
    }

    return Array.from(variables);
}

/**
 * Check if a query contains any variables
 * @param {string} query - The query to check
 * @returns {boolean} - True if query contains variables
 */
export function hasVariables(query) {
    return extractVariables(query).length > 0;
}

/**
 * Substitute variables in an array of queries
 * @param {Array<Object>} queries - Array of query objects
 * @param {Object} variables - Variable values
 * @returns {Array<Object>} - Array of queries with substituted values
 */
export function substituteQueries(queries, variables = {}) {
    if (!Array.isArray(queries)) {
        return queries;
    }

    return queries.map(query => ({
        ...query,
        query: substituteVariables(query.query, variables)
    }));
}

/**
 * Validate that all required variables are provided
 * @param {string} query - The query to validate
 * @param {Object} variables - Provided variables
 * @returns {Object} - {valid: boolean, missing: Array<string>}
 */
export function validateVariables(query, variables = {}) {
    const required = extractVariables(query);
    const missing = required.filter(varName => !(varName in variables));

    return {
        valid: missing.length === 0,
        missing: missing,
        required: required
    };
}

export default {
    substituteVariables,
    extractVariables,
    hasVariables,
    substituteQueries,
    validateVariables
};
